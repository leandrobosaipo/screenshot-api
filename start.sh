#!/bin/bash

# Inicia o worker do Celery em background
celery -A celery_config worker --loglevel=info &

# Inicia a API FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 