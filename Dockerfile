# Usa uma imagem base do Python
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    netcat-traditional \
    redis-tools \
    curl \
    file \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Cria usuário playwright com UID 1000
RUN groupadd -g 1000 playwright && \
    useradd -u 1000 -g playwright -m playwright

# Copia o script de inicialização antes para garantir permissões
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh && \
    chown playwright:playwright /app/start.sh

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Cria diretórios e ajusta permissões
RUN mkdir -p /tmp/screenshot_cache /ms-playwright && \
    chown -R playwright:playwright /app /tmp/screenshot_cache /ms-playwright

# Define variáveis de ambiente
ENV REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_USER=default \
    CACHE_DIR=/tmp/screenshot_cache \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PYTHONUNBUFFERED=1

# Expõe a porta da aplicação
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Instala navegadores do Playwright Python após instalar dependências Python
RUN python -m playwright install --with-deps

# Troca para o usuário playwright
USER playwright

# Comando padrão
CMD ["bash", "/app/start.sh", "api"] 