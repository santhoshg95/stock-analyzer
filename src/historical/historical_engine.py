from pathlib import Path

import pandas as pd

from src.historical.models.historical_profile import HistoricalProfile
from src.historical.models.stock_dna import StockDNA


class HistoricalEngine:

    def __init__(self, data_directory: str):

        self.data_directory = Path(data_directory)

    def load_history(self, symbol: str) -> pd.DataFrame:

        file = self.data_directory / f"{symbol}.csv"

        return pd.read_csv(file)

    def analyze(self, symbol: str):

        df = self.load_history(symbol)

        profile = HistoricalProfile(symbol=symbol)

        dna = StockDNA(symbol=symbol)

        returns = df["Close"].pct_change().dropna()

        profile.average_weekly_return = returns.mean() * 5

        profile.average_monthly_return = returns.mean() * 21

        profile.annualized_return = returns.mean() * 252

        profile.annualized_volatility = returns.std() * (252 ** 0.5)

        profile.win_rate = (returns > 0).mean()

        profile.positive_months = int((returns > 0).sum())

        profile.negative_months = int((returns < 0).sum())

        profile.consistency_score = profile.win_rate * 100

        profile.historical_score = (
            profile.consistency_score * 0.5
            + profile.annualized_return * 0.3
            - profile.annualized_volatility * 0.2
        )

        if profile.annualized_volatility > 0.40:
            dna.volatility_type = "High"

        elif profile.annualized_volatility > 0.25:
            dna.volatility_type = "Medium"

        else:
            dna.volatility_type = "Low"

        if profile.win_rate > 0.60:
            dna.market_personality = "Reliable"

        elif profile.win_rate > 0.50:
            dna.market_personality = "Balanced"

        else:
            dna.market_personality = "Aggressive"

        return profile, dna