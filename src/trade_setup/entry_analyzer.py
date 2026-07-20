"""
Entry Analyzer

Combines Support/Resistance and Risk Reward
to determine whether the current price is a
good entry point.
"""

from src.market_structure.support_resistance import SupportResistanceEngine
from src.risk.risk_reward import RiskRewardEngine


class EntryAnalyzer:

    @staticmethod
    def analyze(df):

        latest_price = float(df.iloc[-1]["Close"])

        levels = SupportResistanceEngine.calculate(df)

        risk_data = RiskRewardEngine.calculate(
            current_price=latest_price,
            support=levels["support"],
            resistance=levels["resistance"]
        )

        return {

            "current_price": latest_price,

            "support": levels["support"],

            "resistance": levels["resistance"],

            "support_distance": levels["support_distance"],

            "resistance_distance": levels["resistance_distance"],

            "risk": risk_data["risk"],

            "reward": risk_data["reward"],

            "risk_reward": risk_data["risk_reward"],

            "quality": risk_data["quality"],

            "atr": float(df.iloc[-1]["ATR"])

        }
