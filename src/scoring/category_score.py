"""
Category Scoring Engine

Calculates weighted category scores.
"""


class CategoryScoreEngine:

    WEIGHTS = {

        "trend": 25,

        "momentum": 20,

        "volume": 15,

        "market_structure": 15,

        "candlestick": 10,

        "multi_timeframe": 10,

        "risk_reward": 5

    }

    @classmethod
    def calculate(cls, report):

        analysis = report["analysis"]

        entry = report["entry"]

        breakout = report["breakout"]

        scores = {}

        # --------------------------------------------------
        # Trend
        # --------------------------------------------------

        if "BULLISH" in analysis.trend:

            scores["trend"] = 25

        elif "SIDEWAYS" in analysis.trend:

            scores["trend"] = 15

        else:

            scores["trend"] = 5

        # --------------------------------------------------
        # Momentum
        # --------------------------------------------------

        if analysis.rsi >= 55 and analysis.macd_signal == "BULLISH CROSSOVER":

            scores["momentum"] = 20

        elif analysis.rsi >= 45:

            scores["momentum"] = 12

        else:

            scores["momentum"] = 5

        # --------------------------------------------------
        # Volume
        # --------------------------------------------------

        if analysis.relative_volume >= 1.5:

            scores["volume"] = 15

        elif analysis.relative_volume >= 1:

            scores["volume"] = 10

        else:

            scores["volume"] = 5

        # --------------------------------------------------
        # Market Structure
        # --------------------------------------------------

        if entry["support_distance"] < 2:

            scores["market_structure"] = 15

        else:

            scores["market_structure"] = 8

        # --------------------------------------------------
        # Candlestick
        # (Placeholder)
        # --------------------------------------------------

        scores["candlestick"] = 5

        # --------------------------------------------------
        # Multi Timeframe
        # (Placeholder)
        # --------------------------------------------------

        scores["multi_timeframe"] = 5

        # --------------------------------------------------
        # Risk Reward
        # --------------------------------------------------

        rr = entry["risk_reward"]

        if rr >= 3:

            scores["risk_reward"] = 5

        elif rr >= 2:

            scores["risk_reward"] = 4

        elif rr >= 1:

            scores["risk_reward"] = 3

        else:

            scores["risk_reward"] = 1

        total = sum(scores.values())

        return {

            "categories": scores,

            "overall": total

        }