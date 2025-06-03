# Usa a imagem oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Instala as dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Instala o Node.js (necessário para o Playwright)
RUN wget -qO- https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de requisitos
COPY requirements.txt .

# Instala as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Playwright e seus navegadores
RUN playwright install chromium \
    && playwright install-deps

# Copia o código da aplicação
COPY . .

# Cria o diretório de cache
RUN mkdir -p /tmp/screenshot_cache \
    && chmod 777 /tmp/screenshot_cache

# Expõe a porta da aplicação
EXPOSE 8000

# Script de inicialização
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Comando para iniciar a aplicação
CMD ["/start.sh"] 