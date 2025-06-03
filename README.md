# API de Screenshots

API para captura de screenshots de páginas web com suporte a cache e processamento assíncrono.

## Requisitos

- Python 3.11+
- Redis
- Playwright
- Celery
- FastAPI

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/screenshot-api.git
cd screenshot-api
```

2. Crie um ambiente virtual e instale as dependências:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

3. Instale o Playwright:
```bash
playwright install
```

## Configuração

### Ambiente Local (Desenvolvimento)

1. Instale o Redis:
```bash
# Ubuntu/Debian
sudo apt-get install redis-server

# macOS
brew install redis

# Windows
# Baixe e instale do https://github.com/microsoftarchive/redis/releases
```

2. Inicie o Redis:
```bash
# Linux/macOS
sudo service redis-server start
# ou
redis-server

# Windows
redis-server
```

3. Configure as variáveis de ambiente:
```bash
# Crie um arquivo .env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
CACHE_DIR=/tmp/screenshot_cache
```

### Ambiente de Produção (VPS)

1. Instale o Docker e Docker Compose:
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose
```

2. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/screenshot-api.git
cd screenshot-api
```

## Execução

### Desenvolvimento Local (Sem Docker)

1. Inicie o worker do Celery:
```bash
# Usando o módulo principal
celery -A main worker --loglevel=info

# Ou usando o módulo de configuração
celery -A celery_config worker --loglevel=info
```

2. Em outro terminal, inicie a API:
```bash
uvicorn main:app --reload
```

### Desenvolvimento Local (Com Docker)

1. Inicie os serviços:
```bash
docker-compose up -d
```

2. Verifique os logs:
```bash
docker-compose logs -f
```

### Produção (VPS)

1. Inicie os serviços:
```bash
docker-compose up -d
```

2. Verifique se os containers estão rodando:
```bash
docker-compose ps
```

3. Verifique os logs:
```bash
docker-compose logs -f
```

4. Para atualizar a aplicação:
```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Uso da API

### Captura Básica
```bash
curl -X POST "http://localhost:8000/screenshot" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.google.com"}'
```

### Captura com Parâmetros
```bash
curl -X POST "http://localhost:8000/screenshot" \
     -H "Content-Type: application/json" \
     -d '{
       "url": "https://www.google.com",
       "view": "desktop",
       "full_page": true,
       "wait_time": 5000,
       "quality": 80,
       "wait_until": "networkidle",
       "wait_for_images_flag": true,
       "scroll_page_flag": true,
       "no_cache": false
     }'
```

### Verificar Status da Tarefa
```bash
curl "http://localhost:8000/screenshot/status/{task_id}"
```

## Endpoints

### POST /screenshot
Captura um screenshot de uma URL.

**Parâmetros:**
- `url` (string, obrigatório): URL da página
- `view` (string, opcional): Tipo de visualização ("desktop" ou "mobile", padrão: "desktop")
- `full_page` (boolean, opcional): Capturar página inteira (padrão: false)
- `wait_time` (integer, opcional): Tempo de espera em ms (padrão: 0)
- `quality` (integer, opcional): Qualidade do JPEG (1-100, padrão: 80)
- `wait_until` (string, opcional): Evento de carregamento ("load", "domcontentloaded", "networkidle", padrão: "networkidle")
- `wait_for_images_flag` (boolean, opcional): Esperar carregamento de imagens (padrão: true)
- `scroll_page_flag` (boolean, opcional): Rolar página automaticamente (padrão: true)
- `no_cache` (boolean, opcional): Ignorar cache (padrão: false)

### GET /screenshot/status/{task_id}
Verifica o status de uma tarefa de captura.

## Cache

- Os screenshots são armazenados em cache por 24 horas
- O cache é compartilhado entre os workers
- O parâmetro `no_cache=true` força uma nova captura
- O cache é limpo automaticamente após 24 horas
- Limite de cache de 1GB com limpeza automática

## Docker

### Construir a Imagem
```bash
docker build -t screenshot-api .
```

### Executar o Container
```bash
docker run -p 8000:8000 screenshot-api
```

## Solução de Problemas

### Redis não Conecta
1. Verifique se o Redis está rodando:
```bash
# Local
redis-cli ping

# Docker
docker-compose exec redis redis-cli ping
```

2. Verifique as variáveis de ambiente:
```bash
# Local
echo $REDIS_HOST
echo $REDIS_PORT

# Docker
docker-compose exec api env | grep REDIS
```

3. Verifique os logs:
```bash
# Local
tail -f celery.log

# Docker
docker-compose logs -f
```

### Cache não Funciona
1. Verifique o diretório de cache:
```bash
# Local
ls -l /tmp/screenshot_cache

# Docker
docker-compose exec api ls -l /tmp/screenshot_cache
```

2. Verifique as permissões:
```bash
# Local
chmod -R 777 /tmp/screenshot_cache

# Docker
docker-compose exec api chmod -R 777 /tmp/screenshot_cache
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Versão

### v1.0.1 (03/06/2024)
- Melhorias na configuração do Redis para ambiente local e Docker
- Otimização do script de inicialização (start.sh)
- Ajustes nas configurações do Celery para melhor performance
- Documentação atualizada com novos parâmetros e configurações
- Melhorias no sistema de cache com limite de tamanho
- Suporte a diferentes eventos de carregamento de página
- Melhor tratamento de erros e reconexão com Redis 