from src.api.news_api import recuperar_noticias_financeiras
from newsapi import NewsApiClient
from src.ai.finbert import analisar_sentimento

if __name__ == '__main__':

    key_word_list = ["dollar", "market", "currency", "stocks", "crypto", "wall street"]
    noticias = recuperar_noticias_financeiras(NewsApiClient.get_top_headlines, key_word_list)
    analisar_sentimento(noticias)
