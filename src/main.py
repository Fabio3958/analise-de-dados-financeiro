from src.api.news_api import recuperar_noticias_financeiras
from newsapi import NewsApiClient
from src.ai.finbert import analisar_sentimento
from src.service.otimizacao_de_porfolio import otimizar_portfolio

if __name__ == '__main__':

    acoes = ["BBAS3",  # Banco Do Brasil
             "CPLE3",  # Copel
             "PETR4",  # Petrobras
             "MULT3",  # Multiplan
             "BBSE3",  # BB Seguridade
             "EQTL3",  # Equatorial
             "PRIO3",  # Prio
             "MSCD34",  # Mastercard
             "AMZO34",  # Amazon
             "PETR4",  # Petrobras
             "ITUB4",  # Itaú Unibanco
             "WEGE3",  # WEG
             "SUZB3",  # Suzano
             "SBSP3",  # Sabesp
             "TIMS3",  # TIM
             "ELET3",  # Eletrobras
             "POMO4",  # Marcopolo
             "JBSS3"  # JBS
             ]

    acoes2 = ["BBAS3",  # Banco Do Brasil
              "CPLE3",  # Copel
              "PETR4",  # Petrobras
              ]
    """
    noticias = recuperar_noticias_financeiras(NewsApiClient.get_everything, acoes)
    analisar_sentimento(noticias)
    """

    print("---------------------------------------------------------------------------------")
    print("RAZÃO DE SHARPE")
    # sharpe
    for chave, valor in otimizar_portfolio([f"{i}.SA" for i in acoes2], 3).items():
        print(f"{chave}: {valor}")

    print("---------------------------------------------------------------------------------")
    print("RISCO MÍNIMO")
    # min_volume
    for chave, valor in otimizar_portfolio([f"{i}.SA" for i in acoes2], 3, "min_vol").items():
        print(f"{chave}: {valor}")

    print("---------------------------------------------------------------------------------")
    print("MAXIMIZA O RETORNO DE ACORDO COM A AVERSÃO A RISCO - CONSERVADOR")
    # max_return conservador
    for chave, valor in otimizar_portfolio([f"{i}.SA" for i in acoes2], 3, "max_return", 2.0).items():
        print(f"{chave}: {valor}")

    print("---------------------------------------------------------------------------------")
    print("MAXIMIZA O RETORNO DE ACORDO COM A AVERSÃO A RISCO - MODERADO")
    # max_return moderado
    for chave, valor in otimizar_portfolio([f"{i}.SA" for i in acoes2], 3, "max_return", 1.0).items():
        print(f"{chave}: {valor}")

    print("---------------------------------------------------------------------------------")
    print("MAXIMIZA O RETORNO DE ACORDO COM A AVERSÃO A RISCO - AGRESSIVO")
    # max_return agressivo
    for chave, valor in otimizar_portfolio([f"{i}.SA" for i in acoes2], 3, "max_return", 0.5).items():
        print(f"{chave}: {valor}")
