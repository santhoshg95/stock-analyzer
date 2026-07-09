"""
AI Score Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.ai.ai_score_engine import AIScoreEngine
from src.pipeline.analysis_pipeline import AnalysisPipeline


def main():

    pipeline = AnalysisPipeline()

    report = pipeline.analyze("SBIN")

    score_engine = AIScoreEngine()

    score = score_engine.calculate(report)

    print("=" * 100)
    print("AI SCORE")
    print("=" * 100)

    print(f"Market           : {score.market}")

    print(f"Technical        : {score.technical}")

    print()

    print(f"Total Score      : {score.total}")

    print(f"Available Score  : {score.max_available}")

    print(f"Percentage       : {score.percentage}%")

    print("=" * 100)


if __name__ == "__main__":
    main()