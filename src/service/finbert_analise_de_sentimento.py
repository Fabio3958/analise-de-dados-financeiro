from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


def analisar_sentimento(noticias: list[dict]) -> list[dict]:
    """
    Analisa o sentimento de manchetes de notícias usando o modelo FinBERT-PT-BR e salva os resultados em uma planilha Excel.

    :param noticias: Lista de dicionários contendo as notícias retornadas pela NewsAPI.
    :return: None. A função salva os resultados em um arquivo Excel chamado "Analise De Sentimento.xlsx".
    """

    # Verifica se a lista de notícias está vazia
    if not noticias or not isinstance(noticias, list):
        raise ValueError("A entrada deve ser uma lista de dicionários.")

    # Verifica se alguma notícia está sem o campo 'title"
    if not all(item.get("title") for item in noticias):
        raise ValueError(f"Todos os dicionários devem ter o campo 'title'.")

    # Carrega modelo prosusAI/finbert e tokenizer
    nome_modelo = "lucas-leme/FinBERT-PT-BR"

    try:
        modelo = BertForSequenceClassification.from_pretrained(nome_modelo)
        tokenizer = BertTokenizer.from_pretrained(nome_modelo)
    except Exception as e:
        raise RuntimeError(f"Erro no carregamento do modelo ou do tokenizer: {e}")

    # Pipeline de análise de sentimento
    nlp = pipeline("sentiment-analysis", model=modelo, tokenizer=tokenizer)

    # Analisa o sentimento de cada headline
    headlines = [item["title"] for item in noticias]
    tickers = [item["ticker"] for item in noticias]

    resultados = nlp(headlines)
    lista_resultados = [
        {"Ticker": ticker, "Headline": headline, "Sentimento": result["label"], "Score": round(result["score"], 2)}
        for headline, result, ticker in zip(headlines, resultados, tickers)
    ]

    return lista_resultados
