"""
Historical Qualification Engine

Determines whether a stock qualifies for the AI platform
based on configurable historical metrics.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from .intelligence import (
    HistoricalIntelligence,
    HistoricalIntelligenceEngine,
)


@dataclass
class QualificationResult:

    symbol: str

    qualified: bool

    score: float

    passed_rules: int

    total_rules: int

    rules: Dict[str, bool]

    reasons: list[str]


class HistoricalQualificationEngine:

    DEFAULT_RULES = {

        "minimum_overall_score": 60,

        "minimum_cagr": 0.10,

        "minimum_sharpe": 1.00,

        "maximum_volatility": 0.40,

        "maximum_drawdown": 0.35,

        "minimum_win_rate": 0.50,

        "minimum_liquidity_score": 50,

    }

    def __init__(

        self,

        intelligence_engine: Optional[
            HistoricalIntelligenceEngine
        ] = None,

        rules: Optional[Dict[str, Any]] = None,

    ) -> None:

        self.engine = (
            intelligence_engine
            or HistoricalIntelligenceEngine()
        )

        self.rules = self.DEFAULT_RULES.copy()

        if rules:

            self.rules.update(rules)

    # -------------------------------------------------------------

    def qualify(

        self,

        symbol: str,

        period: str = "10y",

    ) -> QualificationResult:

        profile = self.engine.analyze(

            symbol,

            period,

        )

        return self.evaluate(profile)

    # -------------------------------------------------------------

    def evaluate(

        self,

        profile: HistoricalIntelligence,

    ) -> QualificationResult:

        stats = profile.statistics

        checks = {

            "overall_score":

                stats.get(
                    "overall_score",
                    0,
                )

                >= self.rules[
                    "minimum_overall_score"
                ],

            "cagr":

                stats.get(
                    "cagr",
                    0,
                )

                >= self.rules[
                    "minimum_cagr"
                ],

            "sharpe":

                stats.get(
                    "sharpe_ratio",
                    0,
                )

                >= self.rules[
                    "minimum_sharpe"
                ],

            "volatility":

                stats.get(
                    "volatility",
                    99,
                )

                <= self.rules[
                    "maximum_volatility"
                ],

            "drawdown":

                abs(

                    stats.get(
                        "max_drawdown",
                        1,
                    )

                )

                <= self.rules[
                    "maximum_drawdown"
                ],

            "win_rate":

                stats.get(
                    "win_rate",
                    0,
                )

                >= self.rules[
                    "minimum_win_rate"
                ],

            "liquidity":

                stats.get(
                    "liquidity_score",
                    0,
                )

                >= self.rules[
                    "minimum_liquidity_score"
                ],

        }

        passed = sum(

            checks.values()

        )

        reasons = []

        for key, passed_rule in checks.items():

            if not passed_rule:

                reasons.append(
                    f"{key} failed"
                )

        score = round(

            (

                passed

                / len(checks)

            )

            * 100,

            2,

        )

        return QualificationResult(

            symbol=profile.symbol,

            qualified=passed == len(checks),

            score=score,

            passed_rules=passed,

            total_rules=len(checks),

            rules=checks,

            reasons=reasons,

        )

    # -------------------------------------------------------------

    def as_dict(

        self,

        symbol: str,

        period: str = "10y",

    ) -> Dict[str, Any]:

        return asdict(

            self.qualify(

                symbol,

                period,

            )

        )

    # -------------------------------------------------------------

    def update_rules(

        self,

        **kwargs,

    ) -> None:

        self.rules.update(kwargs)

    # -------------------------------------------------------------

    def reset_rules(

        self,

    ) -> None:

        self.rules = self.DEFAULT_RULES.copy()

    # -------------------------------------------------------------

    def get_rules(

        self,

    ) -> Dict[str, Any]:

        return self.rules.copy()