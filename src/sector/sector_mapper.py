"""
Sector Mapper

Maps NSE symbols to sectors.
"""

import pandas as pd


class SectorMapper:

    def __init__(self):

        self.df = pd.read_csv("resources/sector_mapping.csv")
        self.df["Symbol"] = self.df["Symbol"].astype(str).str.strip().str.upper().str.removesuffix(".NS")
        self.df["Sector"] = self.df["Sector"].astype(str).str.strip().str.upper()

    def get_sector(self, symbol):

        symbol = str(symbol).strip().upper().removesuffix(".NS")

        result = self.df[self.df["Symbol"] == symbol]

        if result.empty:

            # Never leak an ambiguous UNKNOWN into a report. DIVERSIFIED is a
            # conservative fallback until the symbol is added to the mapping.
            return "DIVERSIFIED"

        return result.iloc[0]["Sector"]

    def get_sector_stocks(self, sector):

        result = self.df[self.df["Sector"] == sector.upper()]

        return result["Symbol"].tolist()

    def get_all_sectors(self):

        return sorted(self.df["Sector"].unique())
