.PHONY: install install-dev clean test lint format check-deps update-deps docker-build docker-up docker-down docker-logs docker-clean

# Variáveis
PYTHON = python3.11
VENV = venv
PIP = $(VENV)/bin/pip
PYTEST = $(VENV)/bin/pytest
BLACK = $(VENV)/bin/black
ISORT = $(VENV)/bin/isort
FLAKE8 = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
PRE_COMMIT = $(VENV)/bin/pre-commit

# Instalação
install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

install-dev: install
	$(PIP) install -e ".[dev]"
	$(PRE_COMMIT) install

# Limpeza
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "*.egg" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

# Testes
test:
	$(PYTEST)

# Linting
lint:
	$(FLAKE8) .
	$(MYPY) .

# Formatação
format:
	$(BLACK) .
	$(ISORT) .

# Verificação de dependências
check-deps:
	$(PIP) check

# Atualização de dependências
update-deps:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt
	$(PIP) install --upgrade -e ".[dev]"

# Docker
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-clean:
	docker-compose down -v
	docker system prune -f

# Ajuda
help:
	@echo "Comandos disponíveis:"
	@echo "  make install        - Instala as dependências"
	@echo "  make install-dev    - Instala as dependências de desenvolvimento"
	@echo "  make clean          - Limpa arquivos temporários"
	@echo "  make test           - Executa os testes"
	@echo "  make lint           - Executa o linting"
	@echo "  make format         - Formata o código"
	@echo "  make check-deps     - Verifica as dependências"
	@echo "  make update-deps    - Atualiza as dependências"
	@echo "  make docker-build   - Constrói as imagens Docker"
	@echo "  make docker-up      - Inicia os containers"
	@echo "  make docker-down    - Para os containers"
	@echo "  make docker-logs    - Mostra os logs dos containers"
	@echo "  make docker-clean   - Limpa os containers e volumes" 