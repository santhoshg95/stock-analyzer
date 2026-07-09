"""
Candidate Scanner Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.candidate.candidate_ranker import CandidateRanker
from src.candidate.candidate_scanner import CandidateScanner
from src.universe.fo_universe import FOUniverse


def main():

    universe = FOUniverse()

    symbols = universe.get_symbols()

    # Scan first 20 stocks initially
    symbols = symbols[:20]

    scanner = CandidateScanner(workers=5)

    results = scanner.scan(symbols)

    ranked = CandidateRanker.rank(results)

    print("=" * 100)
    print("TOP CANDIDATES")
    print("=" * 100)

    print(

        f"{'Rank':<5}"

        f"{'Symbol':<18}"

        f"{'Score':<10}"

        f"{'Percent':<12}"

        f"{'Market':<12}"

        f"{'Technical':<12}"

    )

    print("-" * 100)

    for i, candidate in enumerate(ranked, start=1):

        print(

            f"{i:<5}"

            f"{candidate.symbol:<18}"

            f"{candidate.score:<10.2f}"

            f"{candidate.percentage:<12.2f}"

            f"{candidate.market:<12}"

            f"{candidate.technical:<12}"

        )

    print("=" * 100)


if __name__ == "__main__":
    main()