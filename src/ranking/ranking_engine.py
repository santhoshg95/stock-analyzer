"""
Opportunity Ranking Engine

Combines multiple analysis modules
into a single Opportunity Score.
"""


class RankingEngine:

    WEIGHTS = {

        "technical": 40,

        "relative_strength": 20,

        "market": 15,

        "sector": 15,

        "strategy": 10

    }

    @classmethod
    def calculate(

        cls,

        technical_score,

        rs_rating,

        market_trend,

        sector_trend,

        strategy_name

    ):

        score = 0

        # ----------------------------------------
        # Technical
        # ----------------------------------------

        score += technical_score * 0.40

        # ----------------------------------------
        # Relative Strength
        # ----------------------------------------

        rs_points = {

            "VERY STRONG": 20,

            "STRONG": 17,

            "OUTPERFORM": 14,

            "INLINE": 8,

            "UNDERPERFORM": 0

        }

        score += rs_points.get(rs_rating, 0)

        # ----------------------------------------
        # Market
        # ----------------------------------------

        if "BULLISH" in market_trend:

            score += 15

        elif "SIDEWAYS" in market_trend:

            score += 8

        # ----------------------------------------
        # Sector
        # ----------------------------------------

        if sector_trend == "STRONG":

            score += 15

        elif sector_trend == "BULLISH":

            score += 10

        elif sector_trend == "SIDEWAYS":

            score += 5

        # ----------------------------------------
        # Strategy
        # ----------------------------------------

        if strategy_name != "NO TRADE":

            score += 10

        return round(score, 2)