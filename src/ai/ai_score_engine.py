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

        if hasattr(analysis, "market") and analysis.market:

            max_score += ScoreWeights.MARKET

            if analysis.market.status == "STRONG":

                score.market = ScoreWeights.MARKET

            elif analysis.market.status == "BULLISH":

                score.market = 12

            elif analysis.market.status == "NEUTRAL":

                score.market = 7

            else:

                score.market = 0

        # -----------------------------------
        # Technical
        # -----------------------------------

        if hasattr(analysis, "technical") and analysis.technical:

            max_score += ScoreWeights.TECHNICAL

            technical_score = getattr(
                analysis.technical,
                "score",
                0
            )

            score.technical = round(
                technical_score
                * ScoreWeights.TECHNICAL
                / 100,
                2
            )

        # -----------------------------------
        # Sector
        # -----------------------------------

        if hasattr(analysis, "sector") and analysis.sector:

            max_score += ScoreWeights.SECTOR

            sector_score = getattr(
                analysis.sector,
                "score",
                0
            )

            score.sector = round(
                sector_score
                * ScoreWeights.SECTOR
                / 100,
                2
            )

        # -----------------------------------
        # Breakout
        # -----------------------------------

        if hasattr(analysis, "breakout") and analysis.breakout:

            max_score += ScoreWeights.BREAKOUT

            breakout_score = getattr(
                analysis.breakout,
                "score",
                0
            )

            score.breakout = round(
                breakout_score
                * ScoreWeights.BREAKOUT
                / 100,
                2
            )

        # -----------------------------------
        # Candlestick
        # -----------------------------------

        if hasattr(analysis, "candlestick") and analysis.candlestick:

            max_score += ScoreWeights.CANDLESTICK

            candlestick_score = getattr(
                analysis.candlestick,
                "score",
                0
            )

            score.candlestick = round(
                candlestick_score
                * ScoreWeights.CANDLESTICK
                / 100,
                2
            )

        # -----------------------------------
        # Relative Strength
        # -----------------------------------

        if hasattr(analysis, "relative_strength") and analysis.relative_strength:

            max_score += ScoreWeights.RELATIVE_STRENGTH

            rs_score = getattr(
                analysis.relative_strength,
                "score",
                0
            )

            score.relative_strength = round(
                rs_score
                * ScoreWeights.RELATIVE_STRENGTH
                / 100,
                2
            )

        # -----------------------------------
        # News
        # -----------------------------------

        if hasattr(analysis, "news") and analysis.news:

            max_score += ScoreWeights.NEWS

            news_score = getattr(
                analysis.news,
                "score",
                0
            )

            score.news = round(
                news_score
                * ScoreWeights.NEWS
                / 100,
                2
            )

        # -----------------------------------
        # Options
        # -----------------------------------

        if hasattr(analysis, "option") and analysis.option:

            max_score += ScoreWeights.OPTION

            option_score = getattr(
                analysis.option,
                "score",
                0
            )

            score.option = round(
                option_score
                * ScoreWeights.OPTION
                / 100,
                2
            )

        # -----------------------------------
        # Final Score
        # -----------------------------------

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

                (score.total / max_score) * 100,

                2

            )

        else:

            score.percentage = 0

        return score