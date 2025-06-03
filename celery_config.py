from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

# Configuração do Redis
REDIS_USER = os.getenv('REDIS_USER', 'default')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'ABF93E2D72196575E616CB41A49EE')
REDIS_HOST = os.getenv('REDIS_HOST', 'criadordigital_redis')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# URL de conexão do Redis
REDIS_URL = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

# Configuração do Celery
celery_app = Celery(
    'screenshot_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['main']
)

# Configurações do Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=180,  # 3 minutos máximo por tarefa
    worker_max_tasks_per_child=30,  # Reinicia o worker após 30 tarefas
    worker_prefetch_multiplier=1,  # Processa uma tarefa por vez
    worker_concurrency=1,  # Apenas 1 worker para economizar memória
    broker_pool_limit=1,  # Limita conexões com Redis
    broker_heartbeat=10,  # Reduz frequência de heartbeat
    task_acks_late=True,  # Confirma tarefas apenas após conclusão
    task_reject_on_worker_lost=True,  # Rejeita tarefas se worker morrer
    broker_connection_retry_on_startup=True  # Adiciona esta linha para resolver o warning
)

# Configurações de cache
CACHE_DIR = os.getenv('CACHE_DIR', '/tmp/screenshot_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Limite de cache para 2GB (considerando outros serviços)
MAX_CACHE_SIZE = 2 * 1024 * 1024 * 1024  # 2GB em bytes
CACHE_EXPIRY = 12 * 60 * 60  # 12 horas em segundos 