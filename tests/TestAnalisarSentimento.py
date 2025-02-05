from unittest.mock import patch

import pytest
from src.ai.finbert import analisar_sentimento


def test_lista_vazia():
    """Verifica se a função lança um ValueError ao receber uma lista vazia."""
    with pytest.raises(ValueError,
                       match="A entrada deve ser uma lista de dicionários."):
        analisar_sentimento([])


def test_entrada_nao_lista():
    """Verifica se a função lança um ValueError ao receber um tipo inválido."""
    entradas_invalidas = [None, "string", 123, {"title": "Notícia"}, object()]
    for entrada in entradas_invalidas:
        with pytest.raises(ValueError,
                           match="A entrada deve ser uma lista de dicionários."):
            analisar_sentimento(entrada)


def test_sem_chave_title():
    """Verifica se a função lança um ValueError ao receber dicionários sem a chave 'title'."""
    noticias_invalidas = [{"headline": "Notícia 1"}, {"titulo": "Notícia 2"}]
    with pytest.raises(ValueError, match="Todos os dicionários devem ter o campo 'title'."):
        analisar_sentimento(noticias_invalidas)


def test_title_none_ou_vazio():
    """Verifica se a função lança um ValueError quando 'title' está None ou vazio."""
    noticias_invalidas = [{"title": None}, {"title": ""}, {"title": " "}]
    with pytest.raises(ValueError, match="Nenhuma manchete válida encontrada para análise."):
        analisar_sentimento(noticias_invalidas)


def test_entrada_valida():
    """Verifica se a função aceita uma lista válida sem erros."""
    noticias_validas = [{"title": "Mercado de ações em alta"}, {"title": "Bitcoin bate recorde"}]
    try:
        analisar_sentimento(noticias_validas)
    except Exception as e:
        pytest.fail(f"Erro inesperado com entrada válida: {e}")


def test_modelo_nao_carrega():
    """Verifica se a função lança um RuntimeError ao falhar ao carregar o modelo."""
    noticias = [{"title": "Exemplo de manchete"}]

    with patch("transformers.BertForSequenceClassification.from_pretrained") as mock_model, \
            patch("transformers.BertTokenizer.from_pretrained") as mock_tokenizer:
        # Simula uma exceção ao carregar o modelo
        mock_model.side_effect = Exception("Erro ao carregar o modelo")
        mock_tokenizer.side_effect = Exception("Erro ao carregar o tokenizer")

        with pytest.raises(RuntimeError, match="Erro no carregamento do modelo ou do tokenizer."):
            analisar_sentimento(noticias)
