"""
Entry Analyzer

Combines Support/Resistance and Risk Reward
to determine whether the current price is a
good entry point.
"""

from src.market_structure.support_resistance import SupportResistanceEngine
from src.trade_plan.trade_plan import TradePlanEngine


class EntryAnalyzer:

    @staticmethod
    def analyze(df):

        latest_price = float(df.iloc[-1]["Close"])

        latest = df.iloc[-1]

        levels = SupportResistanceEngine.calculate(df)

        volume_expanding = float(latest["RVOL"]) >= .9
        bullish_macd = float(latest["MACD"]) > float(latest["MACD_SIGNAL"])
        breakout_probability = (
            (25 if float(latest["RVOL"]) >= 1.2 else 12 if volume_expanding else 0)
            + (25 if bullish_macd else 0)
            + (25 if float(latest["Close"]) > float(latest["EMA20"]) > float(latest["EMA50"]) else 0)
            + (15 if 50 <= float(latest["RSI"]) <= 70 else 5 if float(latest["RSI"]) < 50 else 0)
            + (10 if levels["resistance"] and levels["resistance"] - latest_price < float(latest["ATR"]) else 0)
        )
        # A breakout cannot be rated highly before participation and momentum
        # confirm it, regardless of how attractive the remaining context is.
        if not volume_expanding or not bullish_macd:
            breakout_probability = min(breakout_probability, 60)

        report = {

            "current_price": latest_price,

            "support": levels["support"],

            "resistance": levels["resistance"],

            "next_resistance": levels["next_resistance"],

            "resistance_levels": levels["resistance_levels"],

            "broken_resistance": levels["broken_resistance"],

            "support_distance": levels["support_distance"],

            "resistance_distance": levels["resistance_distance"],

            "risk": None,

            "reward": None,

            "risk_reward": None,

            "quality": "UNKNOWN",

            "atr": float(latest["ATR"]),

            # Technical-only estimate used before market/sector context is
            # available.  The daily workflow replaces it with a contextual
            # estimate before making the final risk decision.
            "breakout_probability": round(breakout_probability, 2),

        }
        plan = TradePlanEngine.generate(report)
        report.update({
            "risk": plan.risk,
            "reward": plan.expected_reward,
            "risk_reward": plan.risk_reward,
            "quality": plan.quality,
            "target_basis": plan.target_basis,
            "target_diagnostics": plan.diagnostics,
        })
        return report
