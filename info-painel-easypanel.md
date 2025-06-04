## 🧩 **Painel do Serviço – `screenshot-api`**

### ⚙️ **Ações Rápidas**

Na parte superior do painel, estão disponíveis os seguintes botões de ação:

* ✅ **Implantar** – Inicia manualmente o processo de build/deploy.
* 🟦 **Abrir em nova aba** (ícone de quadrado com seta) – Acesso direto ao endpoint (se houver URL ativa).
* 📄 **Logs** – Visualização de logs de execução do app.
* ✏️ **Editar Nome ou Mensagem Fixa**
* 🗑️ **Excluir Serviço**

---

### 📊 **Recursos do Container (atualmente zerados)**

* **CPU:** `0.0%`
* **Memória:** `0.0 B`
* **Entrada/Saída de Rede:** `0.0 B / 0.0 B`

---

### 📌 **Mensagem Fixa (opcional)**

* Campo: *"Editar para fixar uma mensagem para este serviço"*
  — Permite anotar instruções, avisos ou lembretes para a equipe.

---

### 📋 **Logs**

* Área dedicada para exibição dos **logs em tempo real** do serviço.
* Ideal para verificar erros de build, inicialização da aplicação ou chamadas HTTP.

---


## 🚀 **Detalhes da Implantação – Projeto `screenshot-api`**

### 🔗 Origem (Fonte do Código)

* **Tipo:** GitHub
* **URL do Repositório:**
  `https://github.com/leandrobosaipo/screenshot-api`
* **Branch:**
  `main`
* **Caminho de Build:**
  `/` (raiz do repositório)

### 🔑 Chave SSH (opcional)

* Para repositórios privados, é necessário gerar e adicionar uma **chave SSH** ao repositório.
  Botão disponível: `Gerar chave SSH`

---

## 🔨 **Build (Configuração de Build)**

### Método de Build Selecionado:

* ✅ **Dockerfile**
  Usa o comando: `docker build`
  Documentação: [docs](https://docs.railway.app/develop/builds#docker)

### Outras opções disponíveis (não selecionadas):

* 🔘 **Buildpacks**
  Permite selecionar buildpacks automaticamente (útil para apps em Node.js, Python, etc).
* 🔘 **Nixpacks**
  Forma alternativa de build utilizando Nix (mais configurável).

### Arquivo de Build:

* **Nome do Arquivo:**
  `Dockerfile`
  (Está na raiz do projeto)

---

## 📦 **Histórico de Deploy & Acionador – Projeto `screenshot-api`**

### ✅ **Histórico de Implantação**

Últimos deploys realizados (com sucesso ✅):

1. **feat: versão 1.0.2 – Melhorias para EasyPanel e correções de bugs**
   ⏱️ Duração: 0–3 segundos
   📆 Horário: Todos feitos há cerca de **4 a 5 horas**
   🔍 Botão de acesso: `Visualizar` (logs e detalhes técnicos de cada build)

> Observação: há um botão **“Carregar Mais”** para visualizar deploys anteriores.

---

### 🔁 **Acionador de Implantação (Webhook de Deploy)**

Este endpoint permite acionar o deploy automaticamente via requisição externa (ex: via n8n, GitHub Actions, etc).

* **URL para acionamento:**

```bash
http://173.212.225.231:3000/api/deploy/41a4b200830cb1e57d9cec51c0b6025d4f7f95e5c05f48b8
```

* **Função:**
  Realizar um novo deploy automaticamente deste serviço.

* **Uso sugerido:**
  Integração com serviços externos como **EasyPanel**, **CI/CD**, **webhooks**, etc.

* 🔐 **Botão disponível:**
  `Atualizar Token de Deploy` – Gera um novo token (invalida a URL anterior).

---


## 🌍 **Variáveis de Ambiente – Projeto `screenshot-api`**

Estas variáveis já estão configuradas e prontas para uso no ambiente da aplicação:

```env
REDIS_HOST=criadordigital_redis
REDIS_PORT=6379
REDIS_USER=default
REDIS_PASSWORD=ABF93E2D72196575E616CB41A49EE
CACHE_DIR=/tmp/screenshot_cache
PYTHONUNBUFFERED=1
PYTHONWRITEBYTECODE=1
TZ=America/Sao_Paulo
LOG_LEVEL=DEBUG
```

---

### 📌 Observações Técnicas

* ✅ O botão **"Criar arquivo .env"** está ativado, ou seja, essas variáveis podem ser automaticamente exportadas via `.env` no ambiente de execução.
* 🕓 O fuso horário está corretamente definido como `America/Sao_Paulo`.
* 📂 O diretório de cache das imagens está definido como `/tmp/screenshot_cache`.
* 🐍 Configurações de otimização Python:

  * `PYTHONUNBUFFERED=1` → logs aparecem imediatamente no console.
  * `PYTHONWRITEBYTECODE=1` → permite geração de arquivos `.pyc`.

---

## 🌐 **Domínios Configurados – Projeto `screenshot-api`**

### ✅ Domínio Ativo com HTTPS (externo)

* **URL Pública (HTTPS):**
  `https://screenshot-api-screenshot-api.ujhifl.easypanel.host`

* **Rota Exposta Internamente (destino):**
  `http://screenshot-api_screenshot-api:8000/`

* 🔰 **Protocolo Interno:** HTTP

* 🔁 **Porta Interna:** 8000

* 🌍 **Caminho:** `/`

* ✅ HTTPS ativado para o domínio público

---

### ✏️ Configurações Técnicas do Proxy (conforme o modal de edição)

* **Host (público):**
  `screenshot-api-screenshot-api.ujhifl.easypanel.host`

* **Caminho de Entrada:** `/`

* **Destino Interno:**

  * Protocolo: `HTTP`
  * Porta: `8000`
  * Caminho: `/`

---

## 🗂️ **Montagens e Backups – Projeto `screenshot-api`**

### 📦 **Montagens de Volume (Persistência de Dados)**

**Importante:**
Como o serviço está rodando em Docker, ao ser reiniciado ele **perderá todos os dados não persistidos**. Para evitar isso, o painel oferece 3 tipos de montagem (nenhuma configurada ainda):

* 🔘 **Adicionar Montagem Bind**
* 🔘 **Adicionar Montagem de Volume**
* 🔘 **Adicionar Montagem de Arquivo**

👉 Essas opções permitem **persistir diretórios ou arquivos específicos** no container, como:

* Caches
* Arquivos de configuração
* Logs
* Pastas de upload

📚 Link para ajuda: botão “aqui” no texto “Leia mais sobre montagens”.

---

### 🔒 **Backups de Volume**

* 📂 **Status atual:**
  *“Não há backups de volume no momento”*

* 🛠️ **Botão disponível:**
  `Criar Backup de Volume` – Permite gerar uma cópia de segurança manualmente.

---

## ⚙️ **Configurações Avançadas de Deploy – Projeto `screenshot-api`**

### 🔌 **Portas**

* Nenhuma porta customizada está adicionada.
* ⚠️ Nota:
  Para exportar portas **HTTP/HTTPS**, utilize a aba **Domínios** com proxy reverso.
  Esta seção é usada para **portas internas não web**.

---

### 🚀 **Implantação Personalizada**

* **Réplicas:**
  `1` (padrão – 1 instância do container)

* **Comando customizado:**
  *(vazio)* — nenhum comando personalizado foi definido para o container no momento.

* ✅ **Tempo de inatividade zero:**
  **Ativado** (deploy sem downtime)

* 🟢 **Tini init:**
  **Desativado** (não há uso do init manager Tini)

---

### 🔧 **Permissões e Kernel (opcional)**

* **Adicionar Cap (Capabilities):**
  *(vazio)* — ex: `NET_ADMIN, SYS_MODULE`

* **Remover Cap:**
  *(vazio)*

* **Sysctls personalizados:**

  ```bash
  net.ipv4.ip_forward=1, net.ipv4.conf.all.src_valid_mark=1
  ```

* **Grupos:**
  *(vazio)* — ex: `998, 999`
