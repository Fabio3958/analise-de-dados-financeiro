import yfinance as yf
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return

from src.api.bc_api import recupera_taxa_selic


def recupera_historico_por_prazo(tickers, prazo):
    str_ano = str((datetime.now() - relativedelta(years=prazo)).year)
    primeiro_dia_do_ano = date(int(str_ano), 1, 1)
    return yf.download(tickers, start=primeiro_dia_do_ano, end=str(date.today()))["Close"]


def otimizar_portfolio(acoes):

    df_curto_prazo = recupera_historico_por_prazo(acoes, 3)

    retorno_medio_historico_curto_prazo = mean_historical_return(df_curto_prazo)

    matriz_de_covariancia = CovarianceShrinkage(df_curto_prazo).ledoit_wolf()

    ef = EfficientFrontier(retorno_medio_historico_curto_prazo, matriz_de_covariancia)

    ef.max_sharpe(risk_free_rate=recupera_taxa_selic())
    pesos_arrumados = ef.clean_weights()

    retorno_esperado = ef.portfolio_performance()[0]  # Retorno esperado anualizado
    risco = ef.portfolio_performance()[1]  # Volatilidade (risco)
    sharpe = ef.portfolio_performance()[2]  # Razão de Sharpe

    # Exibir os resultados
    print("Alocação ótima da carteira:", pesos_arrumados)
    print(f"Retorno esperado da carteira: {retorno_esperado:.2%} ao ano")
    print(f"Risco da carteira (volatilidade): {risco:.2%} ao ano")
    print(f"Razão de Sharpe: {sharpe:.2f}")
