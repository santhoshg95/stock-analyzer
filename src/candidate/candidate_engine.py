"""
Candidate Selection Engine

Filters trade opportunities before they are ranked.

Author:
    AI Research Platform
"""

from dataclasses import dataclass, field
from typing import List

from src.models.analysis_result import AnalysisResult


@dataclass
class Candidate:

    symbol: str

    score: float

    passed: bool

    reasons: List[str] = field(default_factory=list)

    warnings: List[str] = field(default_factory=list)


class CandidateEngine:

    DEFAULT_MIN_SCORE = 60.0

    def __init__(

        self,

        minimum_score: float = DEFAULT_MIN_SCORE,

    ):

        self.minimum_score = minimum_score

    # ---------------------------------------------------------

    def evaluate(

        self,

        analysis: AnalysisResult,

        ai_score,

    ) -> Candidate:

        reasons = []

        warnings = []

        passed = True

        score = getattr(ai_score, "percentage", 0)

        # -----------------------------------------------------
        # Technical
        # -----------------------------------------------------

        if analysis.technical:

            if analysis.technical.score >= 70:

                reasons.append(
                    "Technical score meets minimum threshold."
                )

            else:

                warnings.append(
                    "Technical score is below preferred level."
                )

        # -----------------------------------------------------
        # Market
        # -----------------------------------------------------

        if analysis.market:

            if analysis.market.status in (

                "BULLISH",

                "STRONG",

            ):

                reasons.append(
                    "Market trend supports the trade."
                )

            else:

                warnings.append(
                    "Market trend is not favourable."
                )

        # -----------------------------------------------------
        # Sector
        # -----------------------------------------------------

        if analysis.sector:

            if analysis.sector.status in (

                "STRONG",

                "BULLISH",

            ):

                reasons.append(
                    "Sector trend is positive."
                )

            else:

                warnings.append(
                    "Sector is weak."
                )

        # -----------------------------------------------------
        # Relative Strength
        # -----------------------------------------------------

        if analysis.relative_strength:

            if analysis.relative_strength.score >= 70:

                reasons.append(
                    "Relative strength is above average."
                )

            else:

                warnings.append(
                    "Relative strength is weak."
                )

        # -----------------------------------------------------
        # Breakout
        # -----------------------------------------------------

        if analysis.breakout:

            if analysis.breakout.status == "BREAKOUT":

                reasons.append(
                    "Confirmed breakout detected."
                )

        # -----------------------------------------------------
        # Candlestick
        # -----------------------------------------------------

        if analysis.candlestick:

            if analysis.candlestick.score >= 70:

                reasons.append(
                    "Candlestick pattern confirms trade."
                )

        # -----------------------------------------------------
        # Final Decision
        # -----------------------------------------------------

        if score < self.minimum_score:

            passed = False

            warnings.append(
                f"AI Score ({score:.2f}) is below minimum threshold ({self.minimum_score})."
            )

        if len(warnings) >= 4:

            passed = False

        return Candidate(

            symbol=analysis.symbol,

            score=round(score, 2),

            passed=passed,

            reasons=reasons,

            warnings=warnings,

        )

    # ---------------------------------------------------------

    @staticmethod
    def filter(

        candidates: List[Candidate],

    ) -> List[Candidate]:

        return [

            candidate

            for candidate in candidates

            if candidate.passed

        ]

    # ---------------------------------------------------------

    @staticmethod
    def sort(

        candidates: List[Candidate],

    ) -> List[Candidate]:

        return sorted(

            candidates,

            key=lambda x: x.score,

            reverse=True,

        )

    # ---------------------------------------------------------

    def process(

        self,

        analyses: List[AnalysisResult],

        scores,

    ) -> List[Candidate]:

        candidates = []

        for analysis, score in zip(

            analyses,

            scores,

        ):

            candidate = self.evaluate(

                analysis,

                score,

            )

            candidates.append(candidate)

        candidates = self.filter(candidates)

        candidates = self.sort(candidates)

        return candidates