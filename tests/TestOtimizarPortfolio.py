import pytest
from src.service.otimizacao_de_porfolio import otimizar_portfolio


def test_acoes_vazia():
    with pytest.raises(ValueError,
                       match="A lista de ações não pode estar vazia e o número de anos históricos deve ser positivo."):
        otimizar_portfolio([], 5)


def test_anos_historico_negativo():
    with pytest.raises(ValueError,
                       match="A lista de ações não pode estar vazia e o número de anos históricos deve ser positivo."):
        otimizar_portfolio(["AAPL", "MSFT"], -1)


def test_tipo_acoes_incorreto():
    with pytest.raises(ValueError,
                       match="Tipo de parâmetro incorreto: acoes: list\[str\]; anos_historico: int; "
                             "metodo_otimizacao: str"):
        otimizar_portfolio("AAPL", 5)


def test_tipo_anos_historico_incorreto():
    with pytest.raises(ValueError,
                       match="Tipo de parâmetro incorreto: acoes: list\[str\]; anos_historico: int; "
                             "metodo_otimizacao: str"):
        otimizar_portfolio(["AAPL", "MSFT"], "5")


def test_metodo_otimizacao_invalido():
    with pytest.raises(ValueError, match="Método de otimização inválido."):
        otimizar_portfolio(["AAPL", "MSFT"], 5, metodo_otimizacao="invalido")


def test_otimizar_portfolio_sharpe():
    # Dados de entrada
    acoes = ["AAPL", "MSFT", "GOOG"]
    anos_historico = 5
    metodo_otimizacao = "sharpe"

    # Executa a função
    resultado = otimizar_portfolio(acoes, anos_historico, metodo_otimizacao)

    # Verificações
    assert isinstance(resultado, dict)
    assert "alocacao_otima" in resultado
    assert "retorno_esperado" in resultado
    assert "risco" in resultado
    assert "sharpe" in resultado

    # Verifica se a alocação ótima soma 100%
    assert sum(resultado["alocacao_otima"].values()) == pytest.approx(1.0, abs=0.01)


def test_otimizar_portfolio_min_vol():
    # Dados de entrada
    acoes = ["AAPL", "MSFT", "GOOG"]
    anos_historico = 5
    metodo_otimizacao = "min_vol"

    # Executa a função
    resultado = otimizar_portfolio(acoes, anos_historico, metodo_otimizacao)

    # Verificações
    assert isinstance(resultado, dict)
    assert "alocacao_otima" in resultado
    assert "retorno_esperado" in resultado
    assert "risco" in resultado
    assert "sharpe" in resultado

    # Verifica se o risco é menor ou igual ao risco de outros métodos
    risco_min_vol = float(resultado["risco"].rstrip("%"))
    resultado_sharpe = otimizar_portfolio(acoes, anos_historico, metodo_otimizacao="sharpe")
    risco_sharpe = float(resultado_sharpe["risco"].rstrip("%"))
    assert risco_min_vol <= risco_sharpe


def test_otimizar_portfolio_max_return():
    # Dados de entrada
    acoes = ["AAPL", "MSFT", "GOOG"]
    anos_historico = 5
    metodo_otimizacao = "max_return"
    aversao_ao_risco = 1.0

    # Executa a função
    resultado = otimizar_portfolio(acoes, anos_historico, metodo_otimizacao, aversao_ao_risco)

    # Verificações
    assert isinstance(resultado, dict)
    assert "alocacao_otima" in resultado
    assert "retorno_esperado" in resultado
    assert "risco" in resultado
    assert "sharpe" in resultado

    # Verifica se o retorno esperado é maior ou igual ao retorno de outros métodos
    retorno_max_return = float(resultado["retorno_esperado"].rstrip("%"))
    resultado_sharpe = otimizar_portfolio(acoes, anos_historico, metodo_otimizacao="sharpe")
    retorno_sharpe = float(resultado_sharpe["retorno_esperado"].rstrip("%"))
    assert retorno_max_return >= retorno_sharpe
