from collections.abc import Callable
from newsapi import NewsApiClient
from src.config import config


def recuperar_noticias_financeiras(function_news_api: Callable, key_words_list: list[str]) -> list[dict]:

    """
        Busca notícias financeiras usando palavras-chave e uma função da API de notícias.

        :param Callable function_news_api: Função da NewsApiClient (ex: get_top_headlines ou get_everything).
        :param list[str] key_words_list: Lista de palavras chaves a serem pesquisadas.
        :return list[dict] Lista de artigos de notícias encontradas
    """

    article_list = []
    news_api_client = NewsApiClient(config.API_KEY)
    for element in key_words_list:
        try:
            news = function_news_api(news_api_client, q=element)
            articles = news.get("articles", [])
            article_list.extend(articles)
        except Exception as e:
            print(f"Erro ao buscar notícias para {element}: {e}")

    # Retira os titúlos nulos dos dicionários
    article_list = [item for item in article_list if item.get("title")]
    return article_list
