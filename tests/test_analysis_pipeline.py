"""
Analysis Pipeline Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.pipeline.analysis_pipeline import AnalysisPipeline


def main():

    pipeline = AnalysisPipeline()

    report = pipeline.analyze("SBIN")

    print("=" * 100)
    print("COMPLETE ANALYSIS REPORT")
    print("=" * 100)

    print(f"Symbol : {report.symbol}")

    print()

    print("MARKET")
    print("-" * 100)
    print(f"Status      : {report.market.status}")
    print(f"Confidence  : {report.market.confidence}")

    print()

    print("TECHNICAL")
    print("-" * 100)
    print(f"Status      : {report.technical.status}")
    print(f"Score       : {report.technical.score}")
    print(f"Confidence  : {report.technical.confidence}")

    print()

    print("Technical Reasons")

    if report.technical.reasons:
        for reason in report.technical.reasons:
            print(f"✓ {reason}")
    else:
        print("No strong technical reasons generated.")

    print("=" * 100)


if __name__ == "__main__":
    main()