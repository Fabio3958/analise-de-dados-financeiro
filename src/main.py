import yfinance as yf
from numpy import float64


# Apenas iniciando
def obter_preco(ticker: str) -> float64:
    acao = yf.Ticker(ticker)
    preco_atual = acao.history(period='1d')['Close'].iloc[-1]
    return round(preco_atual, 2)


if __name__ == '__main__':
    print(obter_preco('PETR4.SA'))
