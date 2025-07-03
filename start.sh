#!/bin/bash
set -e

# Ajusta permissões do cache
if [ "$(id -u)" = "0" ]; then
  chown -R playwright:playwright /tmp/screenshot_cache || true
  chmod -R 770 /tmp/screenshot_cache || true
else
  # Se não for root, tenta garantir permissão de escrita para todos (último recurso)
  chmod -R a+rwX /tmp/screenshot_cache || true
fi

export PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Debug info
echo "=== Debug Info ==="
whoami
id
ls -la /app/start.sh
echo "SERVICO: $SERVICO"
echo "PLAYWRIGHT_BROWSERS_PATH: $PLAYWRIGHT_BROWSERS_PATH"
echo "================="

# Validação do Playwright
echo "=== Playwright Validation ==="
echo "PLAYWRIGHT_BROWSERS_PATH: $PLAYWRIGHT_BROWSERS_PATH"
ls -la $PLAYWRIGHT_BROWSERS_PATH
if ! find "$PLAYWRIGHT_BROWSERS_PATH" -type f -name "chrome" | grep -q chrome; then
    echo "🛠 Instalando navegadores do Playwright..."
    npx playwright install --with-deps
else
    echo "✅ Navegadores já instalados."
fi
echo "================="

# Função para log
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# Função para verificar se o Redis está disponível
wait_for_redis() {
    log "Aguardando Redis em ${REDIS_HOST}:${REDIS_PORT}..."
    while ! nc -z ${REDIS_HOST} ${REDIS_PORT}; do
        sleep 1
    done
    log "Redis está disponível!"
}

# Função para iniciar o Celery Worker
start_celery() {
    log "Iniciando Celery Worker..."
    celery -A main.celery_app worker --loglevel=info
}

# Função para iniciar o FastAPI
start_api() {
    log "Iniciando FastAPI..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
}

# Verifica se o Redis está disponível
wait_for_redis

# Cria diretório de cache se não existir
mkdir -p ${CACHE_DIR}
chmod 777 ${CACHE_DIR}

# Inicia o serviço apropriado baseado na variável SERVICO
case "${SERVICO}" in
    "celery")
        start_celery
        ;;
    "api")
        start_api
        ;;
    *)
        log "ERRO: Variável SERVICO não definida ou inválida. Use 'api' ou 'celery'."
        exit 1
        ;;
esac 