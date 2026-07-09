"""
Sector Mapper

Maps NSE symbols to sectors.
"""

import pandas as pd


class SectorMapper:

    def __init__(self):

        self.df = pd.read_csv("resources/sector_mapping.csv")

    def get_sector(self, symbol):

        symbol = symbol.upper()

        result = self.df[self.df["Symbol"] == symbol]

        if result.empty:

            return "UNKNOWN"

        return result.iloc[0]["Sector"]

    def get_sector_stocks(self, sector):

        result = self.df[self.df["Sector"] == sector.upper()]

        return result["Symbol"].tolist()

    def get_all_sectors(self):

        return sorted(self.df["Sector"].unique())