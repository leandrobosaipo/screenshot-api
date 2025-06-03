#!/bin/bash

# Função para verificar se o Redis está disponível
wait_for_redis() {
    echo "Aguardando Redis em ${REDIS_HOST}:${REDIS_PORT}..."
    while ! nc -z ${REDIS_HOST} ${REDIS_PORT}; do
        sleep 1
    done
    echo "Redis está disponível!"
}

# Instala netcat para verificar a conexão
apt-get update && apt-get install -y netcat-traditional

# Aguarda o Redis estar disponível
wait_for_redis

# Inicia o worker do Celery em background
celery -A celery_config worker --loglevel=info &

# Inicia a API FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 