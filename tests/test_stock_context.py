"""
Stock Context Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.context.context_builder import ContextBuilder


def main():

    builder = ContextBuilder()

    context = builder.build("SBIN")

    print("=" * 100)
    print("STOCK CONTEXT")
    print("=" * 100)

    print(f"Symbol : {context.symbol}")

    print()

    print("Market")
    print("-" * 100)
    print(f"Status      : {context.market.status}")
    print(f"Confidence  : {context.market.confidence}")

    print()

    print("Technical")
    print("-" * 100)
    print(f"Status      : {context.technical.status}")
    print(f"Confidence  : {context.technical.confidence}")

    print()

    print("AI Score")
    print("-" * 100)
    print("Not calculated yet.")

    print("=" * 100)


if __name__ == "__main__":
    main()