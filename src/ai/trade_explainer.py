"""
Trade Explainer

Generates human-readable explanations for AI trade recommendations.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class TradeExplanation:

    symbol: str

    summary: str

    recommendation: str

    confidence: float

    strengths: List[str]

    risks: List[str]

    execution_plan: List[str]

    monitoring_points: List[str]

    raw_metrics: Dict[str, Any]


class TradeExplainer:

    # ---------------------------------------------------------

    def explain(

        self,

        symbol: str,

        historical: Dict[str, Any],

        strategy: Dict[str, Any],

        options: Dict[str, Any],

        decision: Dict[str, Any],

        confidence: Dict[str, Any],

        portfolio: Dict[str, Any],

    ) -> TradeExplanation:

        strengths = self._strengths(

            historical,

            strategy,

            options,

        )

        risks = self._risks(

            historical,

            options,

        )

        execution = self._execution(

            strategy,

            portfolio,

        )

        monitoring = self._monitoring(

            historical,

            options,

        )

        summary = (

            f"{decision['recommendation']} "

            f"using "

            f"{strategy['strategy']} "

            f"with "

            f"{confidence['confidence']:.2f}% "

            f"confidence."

        )

        metrics = {

            "historical": historical,

            "strategy": strategy,

            "options": options,

            "decision": decision,

            "confidence": confidence,

            "portfolio": portfolio,

        }

        return TradeExplanation(

            symbol=symbol,

            summary=summary,

            recommendation=decision["recommendation"],

            confidence=confidence["confidence"],

            strengths=strengths,

            risks=risks,

            execution_plan=execution,

            monitoring_points=monitoring,

            raw_metrics=metrics,

        )

    # ---------------------------------------------------------

    @staticmethod

    def _strengths(

        historical,

        strategy,

        options,

    ) -> List[str]:

        strengths = []

        if historical.get(

            "overall_score",

            0,

        ) >= 80:

            strengths.append(

                "Strong historical performance."

            )

        if historical.get(

            "sharpe_ratio",

            0,

        ) > 1.5:

            strengths.append(

                "Excellent risk-adjusted returns."

            )

        if historical.get(

            "liquidity_score",

            0,

        ) >= 80:

            strengths.append(

                "Highly liquid security."

            )

        if options.get(

            "iv_rank",

            0,

        ) >= 70:

            strengths.append(

                "High implied volatility supports premium selling."

            )

        if strategy.get(

            "confidence",

            0,

        ) >= 80:

            strengths.append(

                "High strategy confidence."

            )

        return strengths

    # ---------------------------------------------------------

    @staticmethod

    def _risks(

        historical,

        options,

    ) -> List[str]:

        risks = []

        if abs(

            historical.get(

                "max_drawdown",

                0,

            )

        ) > 0.25:

            risks.append(

                "Large historical drawdowns."

            )

        if historical.get(

            "volatility",

            0,

        ) > 0.35:

            risks.append(

                "High historical volatility."

            )

        pcr = options.get(

            "pcr",

            1,

        )

        if pcr > 1.5:

            risks.append(

                "Extreme bullish sentiment."

            )

        elif pcr < 0.5:

            risks.append(

                "Extreme bearish sentiment."

            )

        return risks

    # ---------------------------------------------------------

    @staticmethod

    def _execution(

        strategy,

        portfolio,

    ) -> List[str]:

        plan = [

            f"Execute {strategy['strategy']} strategy.",

            f"Allocate {portfolio.get('allocation',0):.2f} capital.",

            "Verify liquidity before entry.",

            "Use limit orders whenever possible.",

        ]

        return plan

    # ---------------------------------------------------------

    @staticmethod

    def _monitoring(

        historical,

        options,

    ) -> List[str]:

        monitor = [

            "Monitor implied volatility changes.",

            "Monitor option Greeks.",

            "Track open interest shifts.",

            "Watch for earnings/events.",

        ]

        if historical.get(

            "volatility",

            0,

        ) > 0.30:

            monitor.append(

                "Monitor ATR expansion."

            )

        if options.get(

            "iv_rank",

            0,

        ) > 80:

            monitor.append(

                "Monitor IV crush after major events."

            )

        return monitor

    # ---------------------------------------------------------

    @staticmethod

    def export(

        explanation: TradeExplanation,

    ) -> Dict[str, Any]:

        return asdict(explanation)