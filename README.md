# Screenshot API

API simples para capturar screenshots de websites usando FastAPI e Playwright.

## Requisitos

- Python 3.8+
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone este repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Instale os navegadores necessários para o Playwright:
```bash
playwright install
```

## Executando a aplicação

Para iniciar o servidor em modo de desenvolvimento com auto-reload:

```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

## Endpoints

### GET /screenshot

Captura um screenshot de uma URL específica.

Parâmetros:
- `url`: URL do site a ser capturado (ex: https://impactogeral.com.br)
- `view`: Tipo de visualização (`desktop` ou `mobile`)
- `full_page`: Se deve capturar a página inteira (true ou false)
- `wait_time`: Tempo de espera antes de capturar a imagem (em segundos)
- `quality`: Qualidade da imagem (0-100)
- `wait_until`: Condição para esperar antes de capturar a imagem
- `wait_for_images_flag`: Se deve esperar por imagens adicionais
- `scroll_page_flag`: Se deve rolar a página ao capturar a imagem

Exemplo de uso:
```
GET http://localhost:8000/screenshot?url=https://impactogeral.com.br&view=desktop&full_page=true&wait_time=0&quality=80&wait_until=networkidle&wait_for_images_flag=true&scroll_page_flag=true
```

## Resposta

A API retorna uma imagem JPEG com o header `Content-Type: image/jpeg` 