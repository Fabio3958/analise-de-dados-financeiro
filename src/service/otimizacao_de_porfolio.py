import yfinance as yf
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.expected_returns import mean_historical_return

from src.api.bc_api import recupera_taxa_selic


def otimizar_portfolio(acoes: list[str], anos_historico: int, metodo_otimizacao: str = "sharpe",
                       aversao_ao_risco: float = 1.0) -> dict:

    """
    Otimiza o portfólio usando a biblioteca PyPortfolioOpt e dados históricos obtidos via yfinance.

    :param list[str] acoes: Lista de ações que serão usadas para a otimização do portfólio.
    :param int anos_historico: Quantidade de anos no passado para fazer o download do histórico das ações.
    :param str metodo_otimizacao: Método de otimização ('sharpe', 'min_vol', 'max_return').
    :param float aversao_ao_risco: Parâmetro personalizável em caso de uso do método de otimização max_return
    :return: Dicionário contendo a alocação ótima, retornado esperado, risco e índice de Sharpe respectivamente.

    Exemplos:
    >>> otimizar_portfolio(["AAPL", "MSFT", "GOOG"], 5, metodo_otimizacao="sharpe")
    {'alocacao_otima': {'AAPL': 0.4, 'MSFT': 0.3, 'GOOG': 0.3}, 'retorno_esperado': 0.15, 'risco': 0.1, 'sharpe': 1.5}
    """

    if (not isinstance(acoes, list) or not isinstance(anos_historico, int) or not isinstance(metodo_otimizacao, str)
            or not isinstance(aversao_ao_risco, float)):
        raise ValueError("Tipo de parâmetro incorreto: acoes: list[str]; anos_historico: int; metodo_otimizacao: str")

    # Validação de entradas
    if not acoes or anos_historico <= 0:
        raise ValueError("A lista de ações não pode estar vazia e o número de anos históricos deve ser positivo.")

    if metodo_otimizacao not in ["sharpe", "min_vol", "max_return"]:
        raise ValueError(f"Método de otimização inválido."
                         f" Esperado ['sharpe', 'min_vol', 'max_return'], recebido: {metodo_otimizacao}")

    # Download dos dados históricos
    taxa_selic = recupera_taxa_selic()
    str_ano = str((datetime.now() - relativedelta(years=anos_historico)).year)
    primeiro_dia_do_ano = date(int(str_ano), 1, 1)
    try:
        historico = yf.download(acoes, start=primeiro_dia_do_ano, end=str(date.today()))["Close"]
    except Exception as e:
        raise RuntimeError(f"Houve um erro no dowload dos históricos: {e}")

    # Otimização do portfólio
    try:
        retorno_medio_historico_curto_prazo = mean_historical_return(historico)
        matriz_de_covariancia = CovarianceShrinkage(historico).ledoit_wolf()
        ef = EfficientFrontier(retorno_medio_historico_curto_prazo, matriz_de_covariancia)
        if metodo_otimizacao == 'sharpe':
            ef.max_sharpe(risk_free_rate=taxa_selic)
        elif metodo_otimizacao == 'min_vol':
            ef.min_volatility()
        elif metodo_otimizacao == 'max_return':
            ef.max_quadratic_utility(risk_aversion=aversao_ao_risco)

        pesos_arrumados = ef.clean_weights()
        retorno_esperado, risco, sharpe = ef.portfolio_performance(risk_free_rate=taxa_selic)
    except Exception as e:
        raise RuntimeError(f"Houve um erro na otimização do portfólio: {e}")

    # Resultados
    resultados = {
        "alocacao_otima": pesos_arrumados,
        "retorno_esperado": f"{retorno_esperado * 100:.2f}%",
        "risco": f"{risco * 100:.2f}%",
        "sharpe": round(sharpe, 2)
    }

    return resultados
