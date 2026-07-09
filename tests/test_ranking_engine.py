"""
Ranking Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ranking.ranking_engine import RankingEngine


def main():

    score = RankingEngine.calculate(

        technical_score=82,

        rs_rating="VERY STRONG",

        market_trend="STRONG BULLISH",

        sector_trend="STRONG",

        strategy_name="PULLBACK BUY"

    )

    print("=" * 90)
    print("RANKING ENGINE")
    print("=" * 90)

    print(f"Opportunity Score : {score}/100")

    print("=" * 90)


if __name__ == "__main__":
    main()