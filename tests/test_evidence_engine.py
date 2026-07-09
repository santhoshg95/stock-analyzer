"""
Evidence Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.context.context_builder import ContextBuilder
from src.evidence.evidence_engine import EvidenceEngine


def main():

    builder = ContextBuilder()

    context = builder.build("SBIN")

    engine = EvidenceEngine()

    evidence = engine.collect(context)

    print("=" * 100)
    print("AI EVIDENCE")
    print("=" * 100)

    for item in evidence:

        print(f"Source       : {item.source}")
        print(f"Score        : {item.score}")
        print(f"Confidence   : {item.confidence}")
        print(f"Reason       : {item.description}")
        print("-" * 100)


if __name__ == "__main__":
    main()