# Criar pasta "tests" com arquivos "test_xxx.py" from funções "test_xxx" e classes "TestXxxx"
# Rodar "python -m pytest"
# Cobertura: python -m pytest --cov=cripto2 tests/
# Cobertura: python -m pytest --cov=(pasta a ser testada) (node está os testes)

# Teste de integração blackbox (não importa o funcionamento, só o resultado final)

import datetime
from mercado_bitcoin.apis import MercadoBitcoinApi, DaySummaryApi, TradesApi
from mercado_bitcoin.ingestors import DataIngestor, DaySummaryIngestor
from mercado_bitcoin.writers import DataWriter

class TestDaySummaryApi:
    def test_get_data(self):
        actual = DaySummaryApi(coin = "BTC").get_data(date = datetime.date(2022, 6, 1))["date"]
        expect = '2022-06-01'
        assert actual == expect


