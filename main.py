from typing import Literal, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from playwright.async_api import async_playwright
import io

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
    url: str,
    view: Literal["desktop", "mobile"] = "desktop",
    full_page: bool = False,
    wait_time: Optional[int] = 0,
    quality: Optional[int] = 80,
    wait_until: Literal["load", "domcontentloaded", "networkidle"] = "networkidle",
    wait_for_images_flag: bool = True,
    scroll_page_flag: bool = True
) -> Response:
    """
    Endpoint para capturar screenshot de uma URL.
    
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
        Response: Imagem JPEG do screenshot
    """
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
    
    # Captura o screenshot
    screenshot_bytes = await capture_screenshot(
        url=url,
        view=view,
        full_page=full_page,
        wait_time=wait_time,
        quality=quality,
        wait_until=wait_until,
        wait_for_images_flag=wait_for_images_flag,
        scroll_page_flag=scroll_page_flag
    )
    
    # Retorna a imagem com o header apropriado
    return Response(
        content=screenshot_bytes,
        media_type="image/jpeg"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 