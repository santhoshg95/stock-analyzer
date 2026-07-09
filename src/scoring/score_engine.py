"""
Signal Based Score Engine
"""

from typing import List

from src.config.trading_config import (
    BUY,
    NEUTRAL,
    SIGNAL_WEIGHTS,
    STRONG_BUY,
    WATCHLIST,
)

from src.signals.base_signal import Signal


class ScoreEngine:

    @staticmethod
    def calculate(signals: List[Signal]):

        if not signals:

            return {
                "score": 0,
                "max_score": 100,
                "recommendation": "NO SIGNAL"
            }

        weighted_score = 0
        total_weight = 0

        for signal in signals:

            weight = SIGNAL_WEIGHTS.get(signal.name, 0)

            weighted_score += signal.strength * weight
            total_weight += weight

        score = round(weighted_score / total_weight)

        if score >= STRONG_BUY:

            recommendation = "STRONG BUY"

        elif score >= BUY:

            recommendation = "BUY"

        elif score >= WATCHLIST:

            recommendation = "WATCHLIST"

        elif score >= NEUTRAL:

            recommendation = "NEUTRAL"

        else:

            recommendation = "AVOID"

        return {

            "score": score,

            "max_score": 100,

            "recommendation": recommendation

        }