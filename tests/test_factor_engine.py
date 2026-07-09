"""
Factor Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.context.context_builder import ContextBuilder
from src.factors.factor_engine import FactorEngine


def main():

    builder = ContextBuilder()

    context = builder.build("SBIN")

    engine = FactorEngine()

    report = engine.evaluate(context)

    print("=" * 100)
    print("FACTOR ENGINE")
    print("=" * 100)

    for factor in report["factors"]:

        print(f"{factor.name:15} Score : {factor.score}")

        print(f"{'':15} Weight : {factor.weight}")

        print(f"{'':15} Contribution : {factor.contribution:.2f}")

        if factor.reasons:

            print(f"{'':15} Reasons:")

            for reason in factor.reasons:

                print(f"{'':18}✓ {reason}")

        print("-" * 100)

    print()

    print(f"TOTAL SCORE : {report['score']}")

    print("=" * 100)


if __name__ == "__main__":
    main()