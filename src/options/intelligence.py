"""
Options Intelligence Engine

Combines historical intelligence, strategy recommendation and
option chain analytics into a unified intelligence model.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from src.historical.intelligence import HistoricalIntelligenceEngine
from src.strategy.recommender import StrategyRecommendationEngine


@dataclass
class OptionsIntelligence:

    symbol: str

    recommendation: str

    strategy: str

    confidence: float

    historical_score: float

    option_metrics: Dict[str, Any]

    combined_score: float


class OptionsIntelligenceEngine:

    def __init__(

        self,

        historical: Optional[
            HistoricalIntelligenceEngine
        ] = None,

        strategy: Optional[
            StrategyRecommendationEngine
        ] = None,

    ):

        self.historical = (

            historical

            or HistoricalIntelligenceEngine()

        )

        self.strategy = (

            strategy

            or StrategyRecommendationEngine()

        )

    # ---------------------------------------------------------

    def analyze(

        self,

        symbol: str,

        option_chain: Dict[str, Any],

        period: str = "10y",

    ) -> OptionsIntelligence:

        recommendation = self.strategy.recommend(

            symbol,

            period,

        )

        historical = self.historical.analyze(

            symbol,

            period,

        )

        option_metrics = self._extract_option_metrics(

            option_chain

        )

        combined_score = self._combined_score(

            historical.statistics,

            option_metrics,

        )

        return OptionsIntelligence(

            symbol=symbol.upper(),

            recommendation=recommendation.recommendation,

            strategy=recommendation.strategy,

            confidence=recommendation.confidence,

            historical_score=historical.statistics.get(

                "overall_score",

                0,

            ),

            option_metrics=option_metrics,

            combined_score=combined_score,

        )

    # ---------------------------------------------------------

    @staticmethod

    def _extract_option_metrics(

        option_chain: Dict[str, Any],

    ) -> Dict[str, Any]:

        return {

            "iv": option_chain.get("iv", 0),

            "pcr": option_chain.get("pcr", 0),

            "max_pain": option_chain.get("max_pain"),

            "call_oi": option_chain.get("call_oi", 0),

            "put_oi": option_chain.get("put_oi", 0),

            "atm_iv": option_chain.get("atm_iv", 0),

            "iv_rank": option_chain.get("iv_rank", 0),

            "iv_percentile": option_chain.get(

                "iv_percentile",

                0,

            ),

            "call_volume": option_chain.get(

                "call_volume",

                0,

            ),

            "put_volume": option_chain.get(

                "put_volume",

                0,

            ),

        }

    # ---------------------------------------------------------

    @staticmethod

    def _combined_score(

        historical: Dict[str, Any],

        option_metrics: Dict[str, Any],

    ) -> float:

        score = historical.get(

            "overall_score",

            0,

        )

        iv_rank = option_metrics.get(

            "iv_rank",

            0,

        )

        pcr = option_metrics.get(

            "pcr",

            1,

        )

        if iv_rank > 70:

            score += 10

        elif iv_rank > 50:

            score += 5

        if 0.8 <= pcr <= 1.2:

            score += 5

        elif pcr > 1.5:

            score -= 5

        elif pcr < 0.5:

            score -= 5

        return round(

            min(score, 100),

            2,

        )

    # ---------------------------------------------------------

    def summary(

        self,

        symbol: str,

        option_chain: Dict[str, Any],

        period: str = "10y",

    ) -> Dict[str, Any]:

        intelligence = self.analyze(

            symbol,

            option_chain,

            period,

        )

        return asdict(

            intelligence

        )

    # ---------------------------------------------------------

    def health_check(

        self,

        option_chain: Dict[str, Any],

    ) -> bool:

        required = [

            "iv",

            "pcr",

            "call_oi",

            "put_oi",

        ]

        return all(

            key in option_chain

            for key in required

        )