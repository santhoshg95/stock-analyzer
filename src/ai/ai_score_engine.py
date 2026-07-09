"""
AI Score Engine
"""

from src.ai.score_weights import ScoreWeights
from src.models.ai_score import AIScore


class AIScoreEngine:

    def calculate(self, analysis):

        score = AIScore()

        max_score = 0

        # -----------------------------------
        # Market
        # -----------------------------------

        if analysis.market:

            max_score += ScoreWeights.MARKET

            if analysis.market.status == "STRONG":

                score.market = ScoreWeights.MARKET

            elif analysis.market.status == "BULLISH":

                score.market = 12

            elif analysis.market.status == "NEUTRAL":

                score.market = 7

        # -----------------------------------
        # Technical
        # -----------------------------------

        if analysis.technical:

            max_score += ScoreWeights.TECHNICAL

            score.technical = round(

                analysis.technical.score
                * ScoreWeights.TECHNICAL
                / 100,

                2

            )

        # Future Engines
        # max_score += ...

        score.total = round(

            score.market
            + score.technical
            + score.sector
            + score.breakout
            + score.candlestick
            + score.relative_strength
            + score.news
            + score.option,

            2

        )

        score.max_available = max_score

        if max_score > 0:

            score.percentage = round(

                score.total / max_score * 100,

                2

            )

        return score