# Usa uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Instala o Node.js (necessário para o Playwright)
RUN wget -qO- https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos primeiro para aproveitar o cache do Docker
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Playwright e seus navegadores
RUN playwright install chromium

# Copia o resto do código
COPY . .

# Cria o diretório de cache
RUN mkdir -p /tmp/screenshot_cache && chmod 777 /tmp/screenshot_cache

# Expõe a porta da aplicação
EXPOSE 8000

# Define as variáveis de ambiente padrão
ENV REDIS_HOST=localhost
ENV REDIS_PORT=6379
ENV REDIS_USER=default
ENV REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
ENV CACHE_DIR=/tmp/screenshot_cache

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"] 