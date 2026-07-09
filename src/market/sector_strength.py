"""
Sector Strength Analyzer

Version 1

Analyzes NSE sector indices
using EMA trend.
"""

import yfinance as yf

from src.indicators.pipeline import IndicatorPipeline


class SectorStrength:

    SECTORS = {

        "BANK": "^NSEBANK",

        "IT": "^CNXIT"

    }

    @classmethod
    def analyze(cls):

        report = {}

        for sector, ticker in cls.SECTORS.items():

            df = yf.download(

                ticker,

                period="1y",

                interval="1d",

                auto_adjust=True,

                progress=False

            )

            if df.empty:

                report[sector] = "UNKNOWN"

                continue

            df = IndicatorPipeline.run(df)

            latest = df.iloc[-1]

            ema20 = float(latest["EMA20"])
            ema50 = float(latest["EMA50"])
            ema200 = float(latest["EMA200"])

            if ema20 > ema50 > ema200:

                trend = "STRONG"

            elif ema20 > ema200:

                trend = "BULLISH"

            elif ema20 < ema50 < ema200:

                trend = "WEAK"

            else:

                trend = "SIDEWAYS"

            report[sector] = trend

        return report