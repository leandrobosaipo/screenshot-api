from typing import Literal, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import Response, JSONResponse
from playwright.async_api import async_playwright
import io
import os
import hashlib
import time
from datetime import datetime, timedelta
import aiofiles
from celery_config import celery_app, CACHE_DIR
import shutil

app = FastAPI(
    title="Screenshot API",
    description="API para capturar screenshots de websites",
    version="1.0.0"
)

# Configurações de viewport para diferentes dispositivos
VIEWPORT_CONFIGS = {
    "desktop": {"width": 1920, "height": 1080},
    "mobile": {"width": 375, "height": 812}
}

# Configurações de cache
CACHE_EXPIRY = 24 * 60 * 60  # 24 horas em segundos
MAX_CACHE_SIZE = 1024 * 1024 * 1024  # 1GB em bytes

def get_cache_path(url: str, view: str, full_page: bool) -> str:
    """Gera um caminho único para o cache baseado nos parâmetros."""
    cache_key = f"{url}_{view}_{full_page}"
    return os.path.join(CACHE_DIR, hashlib.md5(cache_key.encode()).hexdigest() + ".jpg")

async def cleanup_old_cache():
    """Limpa arquivos de cache antigos."""
    try:
        current_time = time.time()
        for filename in os.listdir(CACHE_DIR):
            filepath = os.path.join(CACHE_DIR, filename)
            if os.path.getmtime(filepath) < current_time - CACHE_EXPIRY:
                os.remove(filepath)
    except Exception as e:
        print(f"Erro ao limpar cache: {e}")

async def check_cache_size():
    """Verifica e limpa o cache se exceder o tamanho máximo."""
    try:
        total_size = sum(os.path.getsize(os.path.join(CACHE_DIR, f)) 
                        for f in os.listdir(CACHE_DIR))
        if total_size > MAX_CACHE_SIZE:
            # Remove os arquivos mais antigos primeiro
            files = [(f, os.path.getmtime(os.path.join(CACHE_DIR, f))) 
                    for f in os.listdir(CACHE_DIR)]
            files.sort(key=lambda x: x[1])
            for f, _ in files:
                if total_size <= MAX_CACHE_SIZE * 0.8:  # Limpa até 80% do limite
                    break
                filepath = os.path.join(CACHE_DIR, f)
                total_size -= os.path.getsize(filepath)
                os.remove(filepath)
    except Exception as e:
        print(f"Erro ao verificar tamanho do cache: {e}")

@celery_app.task(name='main.capture_screenshot_task')
def capture_screenshot_task(
    url: str,
    view: str,
    full_page: bool,
    wait_time: int,
    quality: int,
    wait_until: str,
    wait_for_images_flag: bool,
    scroll_page_flag: bool,
    no_cache: bool = False
) -> str:
    """Tarefa Celery para capturar screenshot."""
    try:
        import asyncio
        from playwright.sync_api import sync_playwright
        import time
        
        cache_path = get_cache_path(url, view, full_page)
        
        # Se no_cache for True, remove o arquivo de cache se existir
        if no_cache and os.path.exists(cache_path):
            os.remove(cache_path)
        
        # Usa a versão síncrona do Playwright para a tarefa Celery
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(viewport=VIEWPORT_CONFIGS[view])
            page = context.new_page()
            
            try:
                # Navega para a URL
                response = page.goto(url, wait_until=wait_until)
                if not response:
                    raise Exception("Falha ao carregar a página")
                
                # Espera o tempo adicional se especificado
                if wait_time > 0:
                    page.wait_for_timeout(wait_time)
                
                # Rola a página se solicitado
                if scroll_page_flag:
                    total_height = page.evaluate("document.body.scrollHeight")
                    viewport_height = page.evaluate("window.innerHeight")
                    current_position = 0
                    while current_position < total_height:
                        page.evaluate(f"window.scrollTo(0, {current_position})")
                        page.wait_for_timeout(500)
                        current_position += viewport_height
                    page.evaluate("window.scrollTo(0, 0)")
                    page.wait_for_timeout(1000)
                
                # Espera imagens carregarem se solicitado
                if wait_for_images_flag:
                    # Espera por todas as imagens visíveis
                    page.evaluate("""() => {
                        return Promise.all(
                            Array.from(document.images)
                                .filter(img => !img.complete)
                                .map(img => new Promise(resolve => {
                                    img.onload = img.onerror = resolve;
                                }))
                        );
                    }""")
                    
                    # Força carregamento de imagens lazy
                    page.evaluate("""() => {
                        const images = document.querySelectorAll('img[loading="lazy"]');
                        images.forEach(img => {
                            if (img.dataset.src) {
                                img.src = img.dataset.src;
                            }
                            if (img.dataset.srcset) {
                                img.srcset = img.dataset.srcset;
                            }
                        });
                    }""")
                    
                    # Espera um pouco mais para garantir que as imagens carregaram
                    page.wait_for_timeout(1000)
                
                # Captura o screenshot
                screenshot_bytes = page.screenshot(
                    type="jpeg",
                    quality=quality,
                    full_page=full_page
                )
                
                # Salva o screenshot no cache
                with open(cache_path, 'wb') as f:
                    f.write(screenshot_bytes)
                
                return cache_path
                
            finally:
                # Garante que o navegador seja fechado mesmo em caso de erro
                try:
                    page.close()
                    context.close()
                    browser.close()
                except Exception as e:
                    print(f"Erro ao fechar o navegador: {e}")
            
    except Exception as e:
        return f"Erro ao capturar screenshot: {str(e)}"

def validate_url(url: str) -> None:
    """
    Valida se a URL fornecida é válida.
    
    Args:
        url: URL a ser validada
        
    Raises:
        HTTPException: Se a URL for inválida
    """
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL inválida. Deve começar com http:// ou https://")

def validate_view(view: str) -> None:
    """
    Valida se o tipo de visualização é suportado.
    
    Args:
        view: Tipo de visualização a ser validado
        
    Raises:
        HTTPException: Se o tipo de visualização não for suportado
    """
    if view not in VIEWPORT_CONFIGS:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de visualização inválido. Use 'desktop' ou 'mobile'"
        )

async def wait_for_images(page) -> None:
    """
    Espera todas as imagens da página carregarem.
    
    Args:
        page: Página do Playwright
    """
    # Espera por todas as imagens visíveis
    await page.evaluate("""() => {
        return Promise.all(
            Array.from(document.images)
                .filter(img => !img.complete)
                .map(img => new Promise(resolve => {
                    img.onload = img.onerror = resolve;
                }))
        );
    }""")
    
    # Força o carregamento de imagens lazy
    await page.evaluate("""() => {
        const images = document.querySelectorAll('img[loading="lazy"]');
        images.forEach(img => {
            if (img.dataset.src) {
                img.src = img.dataset.src;
            }
            if (img.dataset.srcset) {
                img.srcset = img.dataset.srcset;
            }
        });
    }""")
    
    # Espera novamente após forçar o carregamento
    await page.evaluate("""() => {
        return Promise.all(
            Array.from(document.images)
                .filter(img => !img.complete)
                .map(img => new Promise(resolve => {
                    img.onload = img.onerror = resolve;
                }))
        );
    }""")

async def perform_page_scroll(page) -> None:
    """
    Rola a página para carregar conteúdo lazy.
    
    Args:
        page: Página do Playwright
    """
    # Obtém a altura total da página
    total_height = await page.evaluate("document.body.scrollHeight")
    viewport_height = await page.evaluate("window.innerHeight")
    
    # Rola a página em incrementos menores
    current_position = 0
    while current_position < total_height:
        # Rola para a próxima posição
        await page.evaluate(f"window.scrollTo(0, {current_position})")
        # Espera um pouco para o conteúdo carregar
        await page.wait_for_timeout(500)
        # Atualiza a posição
        current_position += viewport_height
    
    # Rola de volta para o topo
    await page.evaluate("window.scrollTo(0, 0)")
    await page.wait_for_timeout(1000)

async def capture_screenshot(
    url: str,
    view: Literal["desktop", "mobile"],
    full_page: bool = False,
    wait_time: int = 0,
    quality: int = 80,
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle",
    wait_for_images_flag: bool = True,
    scroll_page_flag: bool = True
) -> bytes:
    """
    Captura um screenshot da URL fornecida usando o Playwright.
    
    Args:
        url: URL do site a ser capturado
        view: Tipo de visualização (desktop ou mobile)
        full_page: Se True, captura a página inteira incluindo área de rolagem
        wait_time: Tempo de espera em milissegundos após o carregamento da página
        quality: Qualidade do JPEG (1-100)
        wait_until: Quando considerar a página carregada
        wait_for_images_flag: Se True, espera todas as imagens carregarem
        scroll_page_flag: Se True, rola a página para carregar conteúdo lazy
        
    Returns:
        bytes: Imagem do screenshot em formato JPEG
        
    Raises:
        HTTPException: Se houver erro ao capturar o screenshot
    """
    try:
        async with async_playwright() as p:
            # Inicializa o navegador em modo headless
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport=VIEWPORT_CONFIGS[view])
            page = await context.new_page()
            
            # Navega para a URL e espera o carregamento
            await page.goto(url, wait_until=wait_until)
            
            # Espera o tempo adicional se especificado
            if wait_time > 0:
                await page.wait_for_timeout(wait_time)
            
            # Rola a página se solicitado
            if scroll_page_flag:
                await perform_page_scroll(page)
            
            # Espera imagens carregarem se solicitado
            if wait_for_images_flag:
                await wait_for_images(page)
            
            # Captura o screenshot
            screenshot_bytes = await page.screenshot(
                type="jpeg",
                quality=quality,
                full_page=full_page
            )
            
            # Fecha o navegador
            await browser.close()
            
            return screenshot_bytes
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao capturar screenshot: {str(e)}"
        )

@app.get("/screenshot")
async def get_screenshot(
    background_tasks: BackgroundTasks,
    url: str,
    view: Literal["desktop", "mobile"] = "desktop",
    full_page: bool = False,
    wait_time: Optional[int] = 0,
    quality: Optional[int] = 80,
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle",
    wait_for_images_flag: bool = True,
    scroll_page_flag: bool = True,
    no_cache: bool = False
) -> Response:
    """Endpoint para capturar screenshot de uma URL."""
    # Valida os parâmetros
    validate_url(url)
    validate_view(view)
    
    # Valida a qualidade
    if not 1 <= quality <= 100:
        raise HTTPException(
            status_code=400,
            detail="Qualidade deve estar entre 1 e 100"
        )
    
    # Valida o tempo de espera
    if wait_time < 0:
        raise HTTPException(
            status_code=400,
            detail="Tempo de espera não pode ser negativo"
        )
    
    # Verifica cache apenas se no_cache for False
    if not no_cache:
        cache_path = get_cache_path(url, view, full_page)
        if os.path.exists(cache_path):
            if time.time() - os.path.getmtime(cache_path) < CACHE_EXPIRY:
                async with aiofiles.open(cache_path, 'rb') as f:
                    return Response(
                        content=await f.read(),
                        media_type="image/jpeg"
                    )
    
    # Agenda limpeza de cache em background
    background_tasks.add_task(cleanup_old_cache)
    background_tasks.add_task(check_cache_size)
    
    # Envia tarefa para a fila
    task = capture_screenshot_task.delay(
        url=url,
        view=view,
        full_page=full_page,
        wait_time=wait_time,
        quality=quality,
        wait_until=wait_until,
        wait_for_images_flag=wait_for_images_flag,
        scroll_page_flag=scroll_page_flag,
        no_cache=no_cache
    )
    
    return JSONResponse({
        "status": "processing",
        "task_id": task.id,
        "message": "Screenshot está sendo processado"
    })

@app.get("/screenshot/status/{task_id}")
async def get_screenshot_status(task_id: str) -> Response:
    """Endpoint para verificar o status de uma tarefa."""
    task = celery_app.AsyncResult(task_id)
    
    if task.ready():
        if isinstance(task.result, str) and task.result.startswith("Erro"):
            raise HTTPException(status_code=500, detail=task.result)
        
        try:
            async with aiofiles.open(task.result, 'rb') as f:
                return Response(
                    content=await f.read(),
                    media_type="image/jpeg"
                )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    
    return JSONResponse({
        "status": "processing",
        "task_id": task_id
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 