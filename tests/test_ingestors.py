# Criar pasta "tests" com arquivos "test_xxx.py" from funções "test_xxx" e classes "TestXxxx"
# Rodar "python -m pytest"
# Cobertura: python -m pytest --cov=cripto2 tests/
# Cobertura: python -m pytest --cov=(pasta a ser testada) (node está os testes)



import datetime
import pytest
from mercado_bitcoin.ingestors import DataIngestor, DaySummaryIngestor
from mercado_bitcoin.writers import DataWriter
from unittest.mock import mock_open, patch, Mock

@pytest.fixture
def data_ingestor_fixtures():
    return DataIngestor(
            writer = DataWriter,
            coins = ["TEST", "BTC"],
            default_start_date = datetime.datetime(2022,6,1)
        )

#@patch("mercado_bitcoin.ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:

    def test_checkpoint_filename(self, data_ingestor_fixtures):
        actual = data_ingestor_fixtures._checkpoint_filename
        expect = "DataIngestor.checkpoint"
        assert actual == expect
    
    def test_load_checkpoint(self, data_ingestor_fixtures):
        actual = data_ingestor_fixtures._load_checkpoint()
        expect = datetime.datetime(2022,6,1)
        assert actual == expect
    
    @patch("builtins.open", new_callable=mock_open, read_data = '2022-06-20')
    def test_load_checkpoint_existing_checkpoint(self, mock, data_ingestor_fixtures):
        actual = data_ingestor_fixtures._load_checkpoint()
        expect = datetime.date(2022,6,20)
        assert actual == expect
    
    @patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value = None)
    def test_update_checkpoint(self, mock, data_ingestor_fixtures):
        data_ingestor_fixtures._update_checkpoint(datetime.date(2022, 6, 15))
        actual = data_ingestor_fixtures._checkpoint
        expect = datetime.date(2022, 6, 15)
        assert actual == expect
    
    @patch("mercado_bitcoin.ingestors.DataIngestor._write_checkpoint", return_value = None)
    def test_update_checkpoint_written(self, mock, data_ingestor_fixtures):
        data_ingestor_fixtures._update_checkpoint(datetime.date(2022, 6, 15))
        mock.assert_called_once()
    
    @patch("builtins.open", new_callable=mock_open, read_data = '2022-06-20')
    @patch("mercado_bitcoin.ingestors.DataIngestor._checkpoint_filename", return_value = "test.checkpoint")
    def test_write_checkpoint(self, mock_filename, mock_open_file, data_ingestor_fixtures):
        data_ingestor_fixtures._write_checkpoint()
        mock_open_file.assert_called_with(mock_filename, 'w')