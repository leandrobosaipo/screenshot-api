# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.2] - 2024-06-03

### Adicionado
- Endpoint de health check para monitoramento
- Sistema de logs mais robusto em todos os componentes
- Configuração específica para EasyPanel
- Healthcheck no Dockerfile
- Melhor tratamento de erros e reconexão com Redis
- Documentação detalhada para implantação no EasyPanel

### Corrigido
- Problemas de inicialização no EasyPanel
- Configuração do comando de inicialização no Dockerfile
- Permissões do diretório de cache
- Verificação de disponibilidade do Redis
- Configurações de retry do Celery

### Alterado
- Otimização do script de inicialização (start.sh)
- Melhorias nas configurações do Celery para produção
- Atualização da documentação com instruções específicas
- Ajustes nas configurações de cache
- Melhorias no sistema de logs

## [1.0.1] - 2024-06-03

### Adicionado
- Suporte a diferentes eventos de carregamento de página (load, domcontentloaded, networkidle)
- Limite de cache de 1GB com limpeza automática
- Melhor tratamento de erros e reconexão com Redis
- Documentação atualizada com novos parâmetros e configurações

### Corrigido
- Problemas de conexão com Redis em ambiente local
- Configuração de cache para melhor performance
- Tratamento de erros durante captura de screenshots

### Alterado
- Otimização do script de inicialização (start.sh)
- Ajustes nas configurações do Celery para melhor performance
- Melhorias na configuração do Redis para ambiente local e Docker

## [1.0.0] - 2024-06-03

### Adicionado
- Implementação inicial da API de screenshots
- Suporte a captura de screenshots desktop e mobile
- Sistema de cache com expiração de 24 horas
- Processamento assíncrono com Celery
- Configurações personalizáveis de captura
- Suporte a Docker
- Documentação completa
- Endpoint de status de tarefas
- Suporte a captura de página inteira
- Espera por carregamento de imagens
- Scroll automático da página
- Controle de cache via parâmetro no_cache

### Corrigido
- Problemas de conexão com Redis em ambiente local
- Configuração de cache para melhor performance
- Tratamento de erros durante captura de screenshots

### Alterado
- Otimização do Dockerfile para melhor performance
- Melhorias na documentação
- Ajustes nas configurações padrão do Celery 