# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2024-06-03

### Adicionado
- Implementação inicial da API de screenshots
- Suporte para captura de screenshots em desktop e mobile
- Sistema de cache com expiração de 24 horas
- Processamento assíncrono usando Celery
- Configurações personalizáveis para captura
- Suporte para Docker
- Documentação completa
- Endpoint para verificar status das tarefas
- Suporte para captura de página inteira
- Espera por carregamento de imagens
- Rolagem automática da página
- Controle de cache via parâmetro `no_cache`

### Corrigido
- Problemas de conexão com Redis em ambiente local
- Configuração de cache para melhor performance
- Tratamento de erros na captura de screenshots

### Alterado
- Otimização do Dockerfile para melhor performance
- Melhoria na documentação
- Ajuste nas configurações padrão do Celery 