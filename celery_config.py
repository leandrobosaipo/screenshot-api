from celery import Celery
import os
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

# Configuração do Redis
REDIS_USER = os.getenv('REDIS_USER', 'default')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', 'ABF93E2D72196575E616CB41A49EE')
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', '6379')

# URL de conexão do Redis
REDIS_URL = f"redis://{REDIS_USER}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}"

logger.info(f"Conectando ao Redis em {REDIS_HOST}:{REDIS_PORT}")

# Configuração do Celery
celery_app = Celery(
    'screenshot_tasks',
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=['main']
)

# Configurações do Celery
celery_app.conf.update(
    # Serialização
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    
    # Timezone
    timezone='UTC',
    enable_utc=True,
    
    # Configurações de tarefas
    task_track_started=True,
    task_time_limit=180,  # 3 minutos máximo por tarefa
    task_soft_time_limit=150,  # 2.5 minutos soft limit
    task_default_retry_delay=30,  # 30 segundos entre retries
    task_max_retries=3,  # Máximo de 3 tentativas
    
    # Configurações de worker
    worker_max_tasks_per_child=30,  # Reinicia o worker após 30 tarefas
    worker_prefetch_multiplier=1,  # Processa uma tarefa por vez
    worker_concurrency=1,  # Apenas 1 worker para economizar memória
    
    # Configurações de broker
    broker_pool_limit=1,  # Limita conexões com Redis
    broker_heartbeat=10,  # Reduz frequência de heartbeat
    broker_connection_retry=True,  # Tenta reconectar se perder conexão
    broker_connection_retry_on_startup=True,  # Tenta reconectar na inicialização
    broker_connection_max_retries=10,  # Número máximo de tentativas de reconexão
    
    # Configurações de segurança
    task_acks_late=True,  # Confirma tarefas apenas após conclusão
    task_reject_on_worker_lost=True,  # Rejeita tarefas se worker morrer
    
    # Configurações de eventos
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Configurações de resultados
    result_expires=3600,  # Expira resultados após 1 hora
    result_backend_transport_options={
        'retry_policy': {
            'timeout': 5.0
        }
    }
)

# Configurações de cache
CACHE_DIR = os.getenv('CACHE_DIR', '/tmp/screenshot_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Limite de cache para 1GB (considerando outros serviços)
MAX_CACHE_SIZE = 1024 * 1024 * 1024  # 1GB em bytes
CACHE_EXPIRY = 24 * 60 * 60  # 24 horas em segundos

logger.info(f"Cache configurado em {CACHE_DIR} com limite de {MAX_CACHE_SIZE/1024/1024}MB") 