"""
Sector Strength Engine

Calculates today's strength for every sector.
"""

import pandas as pd

from src.market_data.base_provider import BaseMarketProvider


class SectorStrength(BaseMarketProvider):

    def __init__(self):

        self.indices = pd.read_csv("resources/sector_indices.csv")

    def analyze(self):

        report = {}

        for _, row in self.indices.iterrows():

            sector = row["Sector"]

            symbol = row["IndexSymbol"]

            data = self.download_symbol(symbol)

            if data is None:

                continue

            cp = data["change_percent"]

            if cp >= 1:

                rating = "STRONG"

                score = 90

            elif cp > 0:

                rating = "BULLISH"

                score = 75

            elif cp > -1:

                rating = "NEUTRAL"

                score = 55

            else:

                rating = "WEAK"

                score = 30

            report[sector] = {

                "price": data["price"],

                "change_percent": cp,

                "rating": rating,

                "score": score

            }

        return report