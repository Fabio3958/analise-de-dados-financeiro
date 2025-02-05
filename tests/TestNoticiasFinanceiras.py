import unittest
from unittest.mock import MagicMock

from src.api.news_api import recuperar_noticias_financeiras


class TestFinancialNews(unittest.TestCase):

    def setUp(self):
        """Configuração inicial para os testes."""
        self.mock_api = MagicMock()
        self.key_words_list = ["Ações", "Inflação", "Criptomoedas"]

        # Definição do mock do retorno da API
        self.mock_response = {
            "status": "ok",
            "articles": [
                {"title": "Notícia 1", "description": "Descrição 1"},
                {"title": "Notícia 2", "description": "Descrição 2"},
            ]
        }

    def test_get_financial_news(self):
        """Testa se a função retorna os artigos corretamente ao usar um mock."""
        # Configura o mock para sempre retornar a resposta falsa
        self.mock_api.return_value = self.mock_response

        # Chama a função com o mock no lugar da API real
        articles = recuperar_noticias_financeiras(self.mock_api, self.key_words_list)

        # Verifica se o mock foi chamado corretamente
        self.mock_api.assert_called_with(q="Criptomoedas")  # Última palavra-chave

        # Verifica se o resultado contém as notícias mockadas repetidas corretamente
        expected_articles = self.mock_response["articles"] * len(self.key_words_list)
        self.assertEqual(articles, expected_articles)


if __name__ == '__main__':
    unittest.main()
