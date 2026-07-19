"""
Market Regime Engine

Determines the current market regime using trend, momentum,
volatility and market breadth indicators.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any

import pandas as pd


@dataclass
class MarketRegime:

    regime: str

    score: float

    trend_score: float

    momentum_score: float

    volatility_score: float

    breadth_score: float

    confidence: float


class MarketRegimeEngine:

    def evaluate(
        self,
        dataframe: pd.DataFrame,
        indicators: Dict[str, Any],
    ) -> MarketRegime:

        trend = self._trend_score(
            dataframe,
            indicators,
        )

        momentum = self._momentum_score(
            indicators,
        )

        volatility = self._volatility_score(
            indicators,
        )

        breadth = self._breadth_score(
            indicators,
        )

        score = round(
            (
                trend * 0.35
                + momentum * 0.25
                + volatility * 0.20
                + breadth * 0.20
            ),
            2,
        )

        regime = self._classify(score)

        confidence = self._confidence(
            score,
            trend,
            momentum,
            volatility,
            breadth,
        )

        return MarketRegime(
            regime=regime,
            score=score,
            trend_score=trend,
            momentum_score=momentum,
            volatility_score=volatility,
            breadth_score=breadth,
            confidence=confidence,
        )

    # -----------------------------------------------------

    @staticmethod
    def _trend_score(
        dataframe: pd.DataFrame,
        indicators: Dict[str, Any],
    ) -> float:

        sma20 = indicators.get("sma20", 0)
        sma50 = indicators.get("sma50", 0)
        sma200 = indicators.get("sma200", 0)

        price = float(
            dataframe["Close"].iloc[-1]
        )

        score = 0.0

        if price > sma20:
            score += 25

        if price > sma50:
            score += 30

        if price > sma200:
            score += 45

        return score

    # -----------------------------------------------------

    @staticmethod
    def _momentum_score(
        indicators: Dict[str, Any],
    ) -> float:

        rsi = indicators.get("rsi", 50)
        macd = indicators.get("macd", 0)

        score = 50

        if 55 <= rsi <= 70:
            score += 20

        elif rsi > 70:
            score += 10

        elif rsi < 40:
            score -= 20

        if macd > 0:
            score += 20

        return max(
            0,
            min(score, 100),
        )

    # -----------------------------------------------------

    @staticmethod
    def _volatility_score(
        indicators: Dict[str, Any],
    ) -> float:

        atr_percent = indicators.get(
            "atr_percent",
            2,
        )

        vix = indicators.get(
            "vix",
            18,
        )

        score = 100

        if atr_percent > 5:
            score -= 30

        elif atr_percent > 3:
            score -= 15

        if vix > 30:
            score -= 40

        elif vix > 20:
            score -= 20

        return max(
            0,
            score,
        )

    # -----------------------------------------------------

    @staticmethod
    def _breadth_score(
        indicators: Dict[str, Any],
    ) -> float:

        advancing = indicators.get(
            "advancing",
            50,
        )

        declining = indicators.get(
            "declining",
            50,
        )

        total = advancing + declining

        if total == 0:
            return 50

        ratio = advancing / total

        return round(
            ratio * 100,
            2,
        )

    # -----------------------------------------------------

    @staticmethod
    def _classify(
        score: float,
    ) -> str:

        if score >= 90:
            return "STRONG_BULL"

        if score >= 80:
            return "BULL"

        if score >= 65:
            return "WEAK_BULL"

        if score >= 50:
            return "SIDEWAYS"

        if score >= 35:
            return "WEAK_BEAR"

        if score >= 20:
            return "BEAR"

        return "STRONG_BEAR"

    # -----------------------------------------------------

    @staticmethod
    def _confidence(
        score: float,
        trend: float,
        momentum: float,
        volatility: float,
        breadth: float,
    ) -> float:

        spread = max(
            trend,
            momentum,
            volatility,
            breadth,
        ) - min(
            trend,
            momentum,
            volatility,
            breadth,
        )

        confidence = score - (spread * 0.15)

        return round(
            max(
                0,
                min(confidence, 100),
            ),
            2,
        )

    # -----------------------------------------------------

    @staticmethod
    def as_dict(
        regime: MarketRegime,
    ) -> Dict[str, Any]:

        return asdict(regime)