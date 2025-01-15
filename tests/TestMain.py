import unittest
from src.main import obter_preco
from unittest.mock import patch
from pandas import DataFrame


class TestMain(unittest.TestCase):
    @patch('yfinance.Ticker')
    def test_obter_preco(self, mock_ticker):
        mock_ticker.return_value.history.return_value = DataFrame({'Close': [150.0]})
        result = obter_preco('AAPL')
        self.assertEqual(result, 150.0)
