from typing import Callable, List

article_list = []


def get_financial_news(function_news_api: Callable, key_words_list: List[str]) -> List[dict]:

    """
        Busca notícias financeiras usando palavras-chave e uma função da API de notícias.

        Args:
        - function_news_api (Callable: Função da NewsApiClient (ex: get_top_headlines ou get_everything).
        - key_words_lists (List[str]: Lista de palavras chaves a serem pesquisadas).

        Returns:
        List[dict]: Lista de artigos de notícias encontradas
    """

    for element in key_words_list:
        try:
            news = function_news_api(q=element)
            articles = news.get('articles', [])
            article_list.extend(articles)
        except Exception as e:
            print(f'Erro ao buscar notícias para {element}: {e}')

    return article_list
