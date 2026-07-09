"""
Instrument Service
"""

from src.providers.provider_factory import ProviderFactory
from src.repository.instrument_repository import InstrumentRepository


class InstrumentService:

    def __init__(self):

        self.provider = ProviderFactory.create("kite")

        self.repo = InstrumentRepository()

    # ----------------------------------------------------

    def download(self):

        print("Downloading instrument master...")

        df = self.provider.kite.instruments()

        return df

    # ----------------------------------------------------

    def find_equity(self, symbol):

        return self.repo.get_by_symbol(symbol)

    # ----------------------------------------------------

    def get_index_options(self, index_name):

        return self.repo.filter(

            exchange="NFO",

            name=index_name

        )

    # ----------------------------------------------------

    def get_stock_options(self, stock):

        return self.repo.filter(

            exchange="NFO",

            name=stock

        )

    # ----------------------------------------------------

    def get_by_token(self, token):

        return self.repo.get_by_token(token)