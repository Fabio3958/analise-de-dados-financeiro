# Projeto de Análise Financeira

Este projeto é uma ferramenta de análise financeira que combina a recuperação de notícias, análise de sentimento e otimização de portfólio para auxiliar na tomada de decisões financeiras.

## Funcionalidades

1. **Recuperação de Notícias Financeiras**
   - Busca notícias financeiras com base em palavras-chave utilizando uma API de notícias.
   
2. **Análise de Sentimento**
   - Analisa o sentimento de manchetes de notícias utilizando o modelo FinBERT-PT-BR.
   - Salva os resultados da análise em uma planilha Excel para fácil visualização.

3. **Otimização de Portfólio**
   - Otimiza o portfólio utilizando a biblioteca PyPortfolioOpt.
   - Utiliza dados históricos obtidos via `yfinance` para cálculos de otimização.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Pandas**: Para manipulação e análise de dados.
- **PyPortfolioOpt**: Para otimização de portfólio.
- **yfinance**: Para obtenção de dados históricos do mercado financeiro.
- **FinBERT-PT-BR**: Modelo de análise de sentimento em português.

## Instalação
   ```bash
    git clone https://github.com/Fabio3958/AnaliseDeDadosInvestimentos.git
    cd AnaliseDeDadosInvestimentos
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
   ```
## Licença
Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
