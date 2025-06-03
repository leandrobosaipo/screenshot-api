#!/bin/bash

# Função para verificar se o Redis está disponível
wait_for_redis() {
    echo "Aguardando Redis em $REDIS_HOST:$REDIS_PORT..."
    while ! nc -z $REDIS_HOST $REDIS_PORT; do
        sleep 1
    done
    echo "Redis está pronto!"
}

# Verifica se é um worker ou API
if [ "$1" = "worker" ]; then
    # Modo worker
    wait_for_redis
    echo "Iniciando Celery worker..."
    celery -A main worker --loglevel=info
else
    # Modo API
    wait_for_redis
    echo "Iniciando FastAPI..."
    uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
fi 