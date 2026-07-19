"""
IV Rank Analysis
"""

from src.options.models.iv_rank_result import IVRankResult


class IVRankAnalysis:
    """
    Analyze Implied Volatility Rank.
    """

    def analyze(
        self,
        current_iv: float,
        yearly_low_iv: float,
        yearly_high_iv: float,
    ) -> IVRankResult:

        reasons = []

        denominator = yearly_high_iv - yearly_low_iv

        if denominator <= 0:

            return IVRankResult(

                iv_rank=0,

                status="UNKNOWN",

                confidence=0,

                score=50,

                reasons=["Invalid IV history."],
            )

        iv_rank = (
            (current_iv - yearly_low_iv)
            / denominator
        ) * 100

        iv_rank = max(0.0, min(100.0, round(iv_rank, 2)))

        if iv_rank >= 70:

            status = "HIGH_IV"

            confidence = 95

            score = 95

            reasons.append(
                "High IV Rank. Premium selling favorable."
            )

        elif iv_rank >= 40:

            status = "NORMAL_IV"

            confidence = 85

            score = 70

            reasons.append(
                "IV near historical average."
            )

        else:

            status = "LOW_IV"

            confidence = 90

            score = 25

            reasons.append(
                "Low IV Rank. Premium selling less attractive."
            )

        return IVRankResult(

            iv_rank=iv_rank,

            status=status,

            confidence=confidence,

            score=score,

            reasons=reasons,
        )