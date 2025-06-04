# Usa uma imagem base do Python
FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    netcat-traditional \
    redis-tools \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho
WORKDIR /app

# Instala o Node.js (necessário para o Playwright)
RUN wget -qO- https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Configura o diretório do Playwright e instala os navegadores
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
RUN mkdir -p /ms-playwright && \
    playwright install --with-deps chromium && \
    playwright install --with-deps firefox && \
    playwright install --with-deps webkit

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto do código
COPY . .

# Cria o diretório de cache e configura permissões
RUN mkdir -p /tmp/screenshot_cache && \
    chmod 777 /tmp/screenshot_cache && \
    chown -R nobody:nogroup /tmp/screenshot_cache

# Expõe a porta da aplicação
EXPOSE 8000

# Define as variáveis de ambiente padrão
ENV REDIS_HOST=redis \
    REDIS_PORT=6379 \
    REDIS_USER=default \
    CACHE_DIR=/tmp/screenshot_cache \
    PYTHONUNBUFFERED=1

# Script de inicialização
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Comando para iniciar a aplicação
CMD ["./start.sh", "api"] 