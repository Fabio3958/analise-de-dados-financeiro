# Changelog

Este arquivo documenta todas as mudanças importantes do projeto, seguindo o formato Keep a Changelog e utilizando Semantic Versioning.

## [Unreleased]
## [1.1.1] - 2025-08-27
### Added
 - Dialog de aviso com explicações e informações importantes ao usuário

## [1.0.1] - 2025-02-27
### Fixed
- requirements.txt atualizado para sempre puxar a versão mais atualizada do yfinance.

## [1.0.0] - 2025-02-17
### Added
- **Criação da interface interativa** usando Streamlit, permitindo que usuários insiram dados, executem análises e visualizem resultados em tempo real.
- **Deploy da aplicação** no Streamlit Community Cloud, tornando o projeto acessível publicamente.
### Changed
- **BREAKING CHANGE**: A estrutura do projeto foi adaptada para suportar deploy contínuo via GitHub, com configurações de ambiente gerenciadas pelo Streamlit.

## [0.4.0] - 2025-02-10
### Added
- Implementação da funcionalidade de otimização de carteiras de investimento com PyPortfolioOpt e yfinance.

## [0.3.1] - 2025-02-05
### Changed
- Modelo de análise de sentimentos trocado para lucas-leme/FinBERT-PT-BR para suportar a análise de notícias brasileiras.

## [0.3.0] - 2025-02-05
### Added
- Implementação do modelo prosusAI/finbert para a análise de sentimentos das notícias recuperadas.

## [0.2.0] - 2025-01-16
### Added
- Implementação da busca de notícias com NewsAPI. Agora, notícias poderão ser analisadas pela IA.

## [0.1.0] - 2025-01-15
### Added
- Estrutura inicial do projeto.
- Planejamento e definição de funcionalidades principais:
  - Dashboards para visualização de dados financeiros.
  - Análises automatizadas de desempenho de ativos.
  - Uso de algoritmos de IA para geração de carteiras personalizadas.