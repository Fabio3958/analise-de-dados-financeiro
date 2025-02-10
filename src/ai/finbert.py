import openpyxl
from typing import List
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline


def analisar_sentimento(noticias: List[dict]):
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
    resultados = nlp(headlines)
    lista_resultados = [
        {"Headline": headline, "Sentimento": result["label"], "Score": round(result["score"], 2)}
        for headline, result in zip(headlines, resultados)
    ]

    # Cria a planilha com openpyxl
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Análise"

    # Adiciona o cabeçalho e valores
    ws.append(["Headline", "Sentimento", "Score"])
    for resultado in lista_resultados:
        ws.append([resultado["Headline"], resultado["Sentimento"], resultado["Score"]])

    # Ajusta a largura das colunas
    for coluna in ws.columns:
        ws.column_dimensions[coluna[0].column_letter].auto_size = True

    # Salva a planilha
    wb.save("Analise De Sentimento.xlsx")
