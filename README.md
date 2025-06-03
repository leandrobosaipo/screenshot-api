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
  - Controle de cache

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

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Instale os navegadores do Playwright:
```bash
playwright install chromium
```

## Configuração

### Ambiente Local (Desenvolvimento)

1. Instale o Redis (se ainda não tiver):
```bash
brew install redis
```

2. Crie um arquivo `.env` na raiz do projeto:
```bash
# Redis Local
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
CACHE_DIR=/tmp/screenshot_cache
```

3. Inicie o Redis:
```bash
brew services start redis
```

4. Verifique se o Redis está rodando:
```bash
redis-cli ping
# Deve retornar PONG
```

### Ambiente de Produção (VPS)

1. Crie um arquivo `.env` na raiz do projeto:
```bash
# Redis VPS
REDIS_HOST=criadordigital_redis
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
CACHE_DIR=/tmp/screenshot_cache
```

2. Se estiver usando Docker, adicione estas variáveis ao seu `docker-compose.yml` ou comando `docker run`:
```yaml
environment:
  - REDIS_HOST=criadordigital_redis
  - REDIS_PORT=6379
  - REDIS_USER=default
  - REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
  - CACHE_DIR=/tmp/screenshot_cache
```

## Executando o Projeto

### Ambiente Local

1. Inicie o Redis (se ainda não estiver rodando):
```bash
brew services start redis
```

2. Em um terminal, inicie o worker do Celery:
```bash
# Desenvolvimento
celery -A celery_config worker --loglevel=info
```

3. Em outro terminal, inicie a API FastAPI:
```bash
# Desenvolvimento
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Ambiente de Produção

1. Inicie o worker do Celery:
```bash
# Produção
celery -A celery_config worker --loglevel=info --concurrency=1
```

2. Inicie a API FastAPI:
```bash
# Produção
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
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

3. Forçar nova captura ignorando cache:
```bash
curl -X GET "http://localhost:8000/screenshot?url=https://www.google.com&no_cache=true"
```

4. Verificar status da tarefa:
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
- `no_cache` (opcional): Ignora o cache e força nova captura (true/false, padrão: false)

### GET /screenshot/status/{task_id}
Verifica o status de uma tarefa de captura.

## Cache

- Os screenshots são armazenados em cache para otimização
- Cache configurado para 1GB de tamanho máximo
- Expiração do cache após 24 horas
- Limpeza automática de arquivos antigos
- Opção para ignorar cache via parâmetro `no_cache`

## Docker

Para executar com Docker:

1. Construa a imagem:
```bash
docker build -t screenshot-api .
```

2. Execute o container:
```bash
docker run -p 8000:8000 \
  -e REDIS_HOST=host.docker.internal \
  -e REDIS_PORT=6379 \
  -e REDIS_USER=default \
  -e REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE \
  screenshot-api
```

## EasyPanel

Para executar no EasyPanel:

1. Certifique-se de que o Dockerfile está configurado corretamente
2. No EasyPanel, crie um novo serviço usando o Dockerfile
3. Configure as variáveis de ambiente necessárias:
   - REDIS_HOST
   - REDIS_PORT
   - REDIS_USER
   - REDIS_PASSWORD
   - CACHE_DIR
4. Inicie o serviço

## Solução de Problemas

### Redis não conecta

#### Ambiente Local
1. Verifique se o Redis está rodando:
```bash
brew services list
```

2. Teste a conexão com o Redis:
```bash
redis-cli ping
# Deve retornar PONG
```

3. Verifique as variáveis de ambiente:
```bash
cat .env
# Deve mostrar REDIS_HOST=localhost
```

#### Ambiente de Produção
1. Verifique se o Redis está acessível:
```bash
redis-cli -h criadordigital_redis ping
# Deve retornar PONG
```

2. Verifique as variáveis de ambiente:
```bash
cat .env
# Deve mostrar REDIS_HOST=criadordigital_redis
```

3. Se estiver usando Docker, verifique se os containers estão na mesma rede:
```bash
docker network ls
docker network inspect <network_name>
```

### Cache não está funcionando
1. Verifique se o diretório de cache existe:
```bash
ls -la /tmp/screenshot_cache
```

2. Verifique as permissões do diretório:
```bash
chmod 777 /tmp/screenshot_cache
```

3. Verifique o espaço disponível:
```bash
df -h /tmp
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Versionamento

### v1.0.0 (2024-06-03)
- Implementação inicial da API
- Suporte para captura de screenshots
- Sistema de cache
- Processamento assíncrono com Celery
- Configurações personalizáveis
- Suporte para Docker
- Documentação completa 