#!/bin/bash

# Função para log
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Função para verificar se o Redis está disponível
wait_for_redis() {
    log "Aguardando Redis em $REDIS_HOST:$REDIS_PORT..."
    local max_retries=30
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        if nc -z $REDIS_HOST $REDIS_PORT; then
            log "Redis está disponível!"
            return 0
        fi
        log "Redis não está disponível - tentativa $((retry_count + 1)) de $max_retries"
        sleep 2
        retry_count=$((retry_count + 1))
    done
    
    log "ERRO: Não foi possível conectar ao Redis após $max_retries tentativas"
    return 1
}

# Função para configurar o diretório de cache
setup_cache_dir() {
    log "Configurando diretório de cache em $CACHE_DIR"
    if [ ! -d "$CACHE_DIR" ]; then
        mkdir -p "$CACHE_DIR"
    fi
    chmod 777 "$CACHE_DIR"
    chown -R nobody:nogroup "$CACHE_DIR"
    log "Diretório de cache configurado com sucesso"
}

# Função para iniciar o worker do Celery
start_celery_worker() {
    log "Iniciando worker do Celery..."
    celery -A celery_config worker --loglevel=info
}

# Função para iniciar a API FastAPI
start_fastapi() {
    log "Iniciando API FastAPI..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info
}

# Verificar se o Redis está disponível
if ! wait_for_redis; then
    log "ERRO: Falha ao conectar ao Redis. Encerrando..."
    exit 1
fi

# Configurar diretório de cache
setup_cache_dir

# Determinar qual serviço iniciar baseado no argumento
case "$1" in
    "worker")
        start_celery_worker
        ;;
    "api")
        start_fastapi
        ;;
    *)
        log "ERRO: Uso inválido. Uso correto: $0 {worker|api}"
        exit 1
        ;;
esac 