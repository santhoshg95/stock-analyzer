"""
Historical Stock Downloader
"""

import yfinance as yf

from src.config.settings import (
    DATA_FOLDER,
    DEFAULT_INTERVAL,
    DEFAULT_PERIOD,
    NSE_SUFFIX,
)


class StockDownloader:

    def __init__(self):

        DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    def download_stock(
        self,
        symbol,
        period=DEFAULT_PERIOD,
        interval=DEFAULT_INTERVAL,
    ):

        ticker = symbol if symbol.endswith(NSE_SUFFIX) else symbol + NSE_SUFFIX

        print("-" * 60)
        print(f"Downloading : {ticker}")

        try:

            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                auto_adjust=True,
                progress=False,
            )

            if df.empty:
                print("No data available.")
                return None

            file_path = DATA_FOLDER / f"{ticker}.csv"

            df.to_csv(file_path)

            print(f"Rows Saved : {len(df)}")
            print(f"Location   : {file_path}")

            return df

        except Exception as ex:

            print(f"Download Failed : {ticker}")
            print(ex)

            return None