import datetime
import time

from schedule import repeat, every, run_pending
from mercado_bitcoin.apis import MercadoBitcoinApi, DaySummaryApi, TradesApi
from mercado_bitcoin.ingestors import DaySummaryIngestor
from mercado_bitcoin.writers import DataWriter


day_summary_ingestor = DaySummaryIngestor(
    writer=DataWriter,
    coins=["BTC", "ETH", "LTC", "BCH"],
    default_start_date=datetime.date(2022, 6, 15)
)


@repeat(every(1).seconds)
def job():
    day_summary_ingestor.ingest()


while True:
    run_pending()
    time.sleep(0.5)


