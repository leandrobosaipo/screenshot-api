#!/bin/bash

# Função para verificar se o Redis está disponível
wait_for_redis() {
    echo "Aguardando Redis em $REDIS_HOST:$REDIS_PORT..."
    until nc -z $REDIS_HOST $REDIS_PORT; do
        echo "Redis não está disponível - aguardando..."
        sleep 2
    done
    echo "Redis está disponível!"
}

# Função para iniciar o worker do Celery
start_celery_worker() {
    echo "Iniciando worker do Celery..."
    celery -A celery_config worker --loglevel=info
}

# Função para iniciar a API FastAPI
start_fastapi() {
    echo "Iniciando API FastAPI..."
    uvicorn main:app --host 0.0.0.0 --port 8000
}

# Verificar se o Redis está disponível
wait_for_redis

# Determinar qual serviço iniciar baseado no argumento
case "$1" in
    "worker")
        start_celery_worker
        ;;
    "api")
        start_fastapi
        ;;
    *)
        echo "Uso: $0 {worker|api}"
        exit 1
        ;;
esac 