"""
Adaptive AI Score Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.context.context_builder import ContextBuilder
from src.scoring.ai_score_engine_v2 import AIScoreEngineV2


def main():

    builder = ContextBuilder()

    context = builder.build("SBIN")

    engine = AIScoreEngineV2()

    score = engine.calculate(context)

    print("=" * 100)
    print("ADAPTIVE AI SCORE")
    print("=" * 100)

    print(f"Total Score     : {score.total_score}")
    print(f"Max Score       : {score.max_score}")
    print(f"Percentage      : {score.percentage}%")
    print(f"Confidence      : {score.confidence}%")
    print(f"Recommendation  : {score.recommendation}")

    print("\nFactors")
    print("-" * 100)

    for factor in score.factors:

        print(
            f"{factor.name:15}"
            f"Score={factor.score:<6}"
            f"Weight={factor.weight:<5}"
            f"Contribution={factor.contribution:.2f}"
        )

    print("=" * 100)


if __name__ == "__main__":
    main()