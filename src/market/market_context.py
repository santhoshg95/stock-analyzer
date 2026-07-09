"""
Market Context Engine

Analyzes the overall market trend.

Version 1:
- NIFTY 50
"""

import yfinance as yf

from src.indicators.pipeline import IndicatorPipeline


class MarketContext:

    MARKET_SYMBOLS = {

        "NIFTY50": "^NSEI"

    }

    @classmethod
    def analyze(cls):

        report = {}

        for name, ticker in cls.MARKET_SYMBOLS.items():

            df = yf.download(

                ticker,

                period="1y",

                interval="1d",

                auto_adjust=True,

                progress=False

            )

            if df.empty:

                report[name] = {

                    "trend": "UNKNOWN",

                    "close": None

                }

                continue

            df = IndicatorPipeline.run(df)

            latest = df.iloc[-1]

            close = float(latest["Close"])

            ema20 = float(latest["EMA20"])

            ema50 = float(latest["EMA50"])

            ema200 = float(latest["EMA200"])

            if close > ema20 > ema50 > ema200:

                trend = "STRONG BULLISH"

            elif close < ema20 < ema50 < ema200:

                trend = "STRONG BEARISH"

            elif close > ema200:

                trend = "LONG TERM BULLISH"

            else:

                trend = "SIDEWAYS"

            report[name] = {

                "trend": trend,

                "close": round(close, 2)

            }

        return report