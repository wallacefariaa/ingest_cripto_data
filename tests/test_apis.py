# Criar pasta "tests" com arquivos "test_xxx.py" from funções "test_xxx" e classes "TestXxxx"
# Rodar "python -m pytest"
# Cobertura: python -m pytest --cov=cripto2 tests/
# Cobertura: python -m pytest --cov=(pasta a ser testada) (node está os testes)


import datetime
from logging import exception
import pytest
from requests import ReadTimeout, patch
import requests
from mercado_bitcoin.apis import MercadoBitcoinApi, DaySummaryApi, TradesApi
from unittest.mock import mock_open, patch, Mock

class TestDaySummaryApi():
    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            ("BTC", datetime.date(2022, 6, 1),
            "https://www.mercadobitcoin.net/api/BTC/day-summary/2022/6/1/"),
            ("ETH", datetime.date(2022, 6, 1),
            "https://www.mercadobitcoin.net/api/ETH/day-summary/2022/6/1/"),
            ("BTC", datetime.date(2021, 12, 31),
            "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/12/31/"),
            ("ETH", datetime.date(2021, 12, 31),
            "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/12/31/")
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin = coin)
        actual = api._get_endpoint(date = date)
        assert actual == expected

class TestTradesApi():
    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            ("BTC", None, None,
            "https://www.mercadobitcoin.net/api/BTC/trades/"),
            ("ETH", None, None,
            "https://www.mercadobitcoin.net/api/ETH/trades/"),
            ("BTC", datetime.datetime(2021,12,31), None,
            "https://www.mercadobitcoin.net/api/BTC/trades/1640919600/"),
            ("ETH", datetime.datetime(2022,6,1), None,
            "https://www.mercadobitcoin.net/api/ETH/trades/1654052400/"),
            ("BTC", datetime.datetime(2021,12,31), datetime.datetime(2022,3,15),
            "https://www.mercadobitcoin.net/api/BTC/trades/1640919600/1647313200/"),
            ("ETH", datetime.datetime(2022,3,15), datetime.datetime(2022,6,1),
            "https://www.mercadobitcoin.net/api/ETH/trades/1647313200/1654052400/"),
            ("TEST", None, datetime.datetime(2022,6,1),
            "https://www.mercadobitcoin.net/api/TEST/trades/")
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesApi(coin = coin)
        actual = api._get_endpoint(date_from = date_from, date_to = date_to )
        assert actual == expected

    def test_get_endpoint_date_from_greater_than_date_to(self):
        with pytest.raises(RuntimeError):
            api = TradesApi(coin = "TEST")
            api._get_endpoint(
                datetime.datetime(2022,6,1),
                datetime.datetime(2021,12,31)
            )

    @pytest.mark.parametrize(
            "date, expected",
            [
                (datetime.datetime(2021,12,31), 1640919600),
                (datetime.datetime(2022,3,15), 1647313200),
                (datetime.datetime(2022,6,1), 1654052400)
            ]
        )
    def test_unix_epoch(self, date, expected):
        api = TradesApi(coin = "TEST")
        actual = api._get_unix_epoch(date = date)
        assert actual == expected

@pytest.fixture()
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(coin = "TEST")

# Monkey patches
def mocked_requests_get(endpoint: str):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code) -> None:
            super().__init__()
            self.status_code = status_code
            self.json_data = json_data
        
        def json(self):
            return self.json_data

        def raise_for_status(self):
            if self.status_code != 200:
                raise Exception
        
    if endpoint == "valid_endpoint":
        return MockResponse(json_data = {"wallace": "teste"}, status_code = 200)
    else:
        return MockResponse(json_data = None, status_code = 404)


class TestMercadoBitcoinApi():

    @patch("requests.get")
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value = "valid_endpoint")
    def test_get_data_requests_is_called(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api.get_data()
        mock_requests.assert_called_once_with("valid_endpoint")
    
    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value = "valid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {"wallace": "teste"}
        assert actual == expected
    
    @patch("requests.get", side_effect = mocked_requests_get)
    @patch("mercado_bitcoin.apis.MercadoBitcoinApi._get_endpoint", return_value = "invalid_endpoint")
    def test_get_data_with_valid_endpoint(self, mock_get_endpoint, mock_requests, fixture_mercado_bitcoin_api):
        with pytest.raises(Exception):
            fixture_mercado_bitcoin_api.get_data()