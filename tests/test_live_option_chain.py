"""
Live Option Chain Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.option_chain.live_option_chain import LiveOptionChain


def main():

    chain = LiveOptionChain()

    df = chain.build("NIFTY")

    print("=" * 100)

    print("LIVE OPTION CHAIN")

    print("=" * 100)

    print(df.head(20))

    print()

    print(f"Total Contracts : {len(df)}")

    print("=" * 100)


if __name__ == "__main__":
    main()