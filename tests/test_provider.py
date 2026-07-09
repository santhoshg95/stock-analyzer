"""
Provider Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.providers.provider_factory import ProviderFactory


def main():

    provider = ProviderFactory.create("yahoo")

    print("=" * 90)
    print("MARKET DATA PROVIDER")
    print("=" * 90)

    ltp = provider.get_ltp("RELIANCE")

    print(f"LTP : ₹{ltp}")

    print("=" * 90)


if __name__ == "__main__":
    main()