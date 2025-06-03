# API de Screenshots

API para capturar screenshots de websites usando Playwright e Celery para processamento assíncrono.

## Funcionalidades

- Captura de screenshots de websites
- Suporte para visualização desktop e mobile
- Processamento assíncrono com Celery
- Sistema de cache para otimização
- Configurações personalizáveis:
  - Qualidade da imagem
  - Tempo de espera
  - Captura de página inteira
  - Espera por carregamento de imagens
  - Rolagem automática da página

## Requisitos

- Python 3.11+
- Redis
- Playwright
- Celery
- FastAPI

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd screenshot
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Instale os navegadores do Playwright:
```bash
playwright install chromium
```

## Configuração

1. Configure as variáveis de ambiente (opcional):
```bash
REDIS_URL=redis://localhost:6379/0
CACHE_DIR=/tmp/screenshot_cache
```

## Executando o Projeto

1. Inicie o Redis:
```bash
# macOS
brew services start redis

# Linux
sudo systemctl start redis
```

2. Em um terminal, inicie o worker do Celery:
```bash
celery -A celery_config worker --loglevel=info
```

3. Em outro terminal, inicie a API FastAPI:
```bash
uvicorn main:app --reload
```

## Testando a API

1. Captura básica:
```bash
curl -X GET "http://localhost:8000/screenshot?url=https://www.google.com&view=desktop"
```

2. Captura com parâmetros personalizados:
```bash
curl -X GET "http://localhost:8000/screenshot?url=https://www.google.com&view=desktop&full_page=true&wait_time=2000&quality=90"
```

3. Verificar status da tarefa:
```bash
curl -X GET "http://localhost:8000/screenshot/status/{task_id}"
```

## Endpoints da API

### GET /screenshot
Captura um screenshot de uma URL.

Parâmetros:
- `url` (obrigatório): URL do site a ser capturado
- `view` (opcional): Tipo de visualização ("desktop" ou "mobile", padrão: "desktop")
- `full_page` (opcional): Captura página inteira (true/false, padrão: false)
- `wait_time` (opcional): Tempo de espera em ms após carregamento (padrão: 0)
- `quality` (opcional): Qualidade do JPEG 1-100 (padrão: 80)
- `wait_until` (opcional): Quando considerar a página carregada ("load", "domcontentloaded", "networkidle", padrão: "networkidle")
- `wait_for_images_flag` (opcional): Espera imagens carregarem (true/false, padrão: true)
- `scroll_page_flag` (opcional): Rola a página (true/false, padrão: true)

### GET /screenshot/status/{task_id}
Verifica o status de uma tarefa de captura.

## Cache

- Os screenshots são armazenados em cache para otimização
- Cache configurado para 2GB de tamanho máximo
- Expiração do cache após 12 horas
- Limpeza automática de arquivos antigos

## Docker

Para executar com Docker:

1. Construa a imagem:
```bash
docker build -t screenshot-api .
```

2. Execute o container:
```bash
docker run -p 8000:8000 screenshot-api
```

## EasyPanel

Para executar no EasyPanel:

1. Certifique-se de que o Dockerfile está configurado corretamente
2. No EasyPanel, crie um novo serviço usando o Dockerfile
3. Configure as variáveis de ambiente necessárias
4. Inicie o serviço

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request 