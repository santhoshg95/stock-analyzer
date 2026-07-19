"""
Options Strategy Selector

Selects the most appropriate options strategy based on
historical intelligence, options intelligence and market metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from .intelligence import (
    OptionsIntelligence,
    OptionsIntelligenceEngine,
)


@dataclass
class SelectedStrategy:

    symbol: str

    strategy: str

    confidence: float

    risk_level: str

    expected_market: str

    rationale: list[str]

    metrics: Dict[str, Any]


class OptionsStrategySelector:

    def __init__(
        self,
        intelligence: Optional[
            OptionsIntelligenceEngine
        ] = None,
    ):

        self.intelligence = (
            intelligence
            or OptionsIntelligenceEngine()
        )

    # --------------------------------------------------------

    def select(
        self,
        symbol: str,
        option_chain: Dict[str, Any],
        period: str = "10y",
    ) -> SelectedStrategy:

        profile = self.intelligence.analyze(
            symbol,
            option_chain,
            period,
        )

        metrics = profile.option_metrics

        strategy, reasons = self._determine_strategy(
            profile,
            metrics,
        )

        return SelectedStrategy(

            symbol=symbol.upper(),

            strategy=strategy,

            confidence=profile.combined_score,

            risk_level=self._risk_level(profile),

            expected_market=self._market_outlook(metrics),

            rationale=reasons,

            metrics=metrics,

        )

    # --------------------------------------------------------

    def as_dict(
        self,
        symbol: str,
        option_chain: Dict[str, Any],
        period: str = "10y",
    ) -> Dict[str, Any]:

        return asdict(
            self.select(
                symbol,
                option_chain,
                period,
            )
        )

    # --------------------------------------------------------

    def _determine_strategy(
        self,
        profile: OptionsIntelligence,
        metrics: Dict[str, Any],
    ):

        reasons = []

        iv_rank = metrics.get("iv_rank", 0)
        pcr = metrics.get("pcr", 1.0)
        confidence = profile.combined_score

        recommendation = profile.recommendation.upper()

        if recommendation == "STRONG BUY":

            if iv_rank >= 70:

                reasons.append(
                    "High IV favors premium selling."
                )

                return "Cash Secured Put", reasons

            reasons.append(
                "Bullish trend with moderate volatility."
            )

            return "Bull Put Spread", reasons

        if recommendation == "BUY":

            if iv_rank >= 70:

                reasons.append(
                    "High IV with bullish bias."
                )

                return "Covered Call", reasons

            reasons.append(
                "Bullish directional opportunity."
            )

            return "Bull Put Spread", reasons

        if recommendation == "WATCH":

            if 0.8 <= pcr <= 1.2:

                reasons.append(
                    "Neutral PCR indicates range-bound market."
                )

                return "Iron Condor", reasons

            if iv_rank >= 60:

                reasons.append(
                    "Elevated IV favors premium collection."
                )

                return "Iron Butterfly", reasons

            reasons.append(
                "Waiting for confirmation."
            )

            return "Calendar Spread", reasons

        if confidence < 50:

            reasons.append(
                "Low confidence environment."
            )

            return "No Trade", reasons

        reasons.append(
            "Bearish conditions detected."
        )

        return "Bear Call Spread", reasons

    # --------------------------------------------------------

    @staticmethod
    def _risk_level(
        profile: OptionsIntelligence,
    ) -> str:

        score = profile.combined_score

        if score >= 85:
            return "LOW"

        if score >= 65:
            return "MEDIUM"

        return "HIGH"

    # --------------------------------------------------------

    @staticmethod
    def _market_outlook(
        metrics: Dict[str, Any],
    ) -> str:

        pcr = metrics.get("pcr", 1.0)

        if pcr > 1.3:
            return "BULLISH"

        if pcr < 0.7:
            return "BEARISH"

        return "NEUTRAL"

    # --------------------------------------------------------

    def explain(
        self,
        symbol: str,
        option_chain: Dict[str, Any],
        period: str = "10y",
    ) -> str:

        result = self.select(
            symbol,
            option_chain,
            period,
        )

        lines = [

            f"Symbol: {result.symbol}",

            f"Selected Strategy: {result.strategy}",

            f"Confidence: {result.confidence:.2f}%",

            f"Risk Level: {result.risk_level}",

            f"Expected Market: {result.expected_market}",

            "",

            "Reasons:",

        ]

        for reason in result.rationale:

            lines.append(f"- {reason}")

        return "\n".join(lines)