"""
Data Provider

Responsibilities:
1. Check whether local historical data exists.
2. Load data from CSV if available.
3. Download fresh data if CSV does not exist.
4. Save downloaded data.
"""

from pathlib import Path

import pandas as pd

from src.config.settings import DATA_FOLDER
from src.data_collection.downloader import StockDownloader


class DataProvider:

    def __init__(self):

        self.downloader = StockDownloader()

    def get_data(self, symbol: str):

        csv_file = DATA_FOLDER / f"{symbol}.NS.csv"

        # ---------------------------------------------
        # Local File Exists
        # ---------------------------------------------

        if csv_file.exists():

            print(f"Loading cached data : {symbol}")

            df = pd.read_csv(
                csv_file,
                header=[0, 1],
                index_col=0,
                parse_dates=True
            )

            # Flatten MultiIndex columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            return df

        # ---------------------------------------------
        # Download
        # ---------------------------------------------

        print(f"No cache found : {symbol}")

        df = self.downloader.download_stock(symbol)

        if df is None:
            return None

        return df