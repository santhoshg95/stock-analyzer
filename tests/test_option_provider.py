"""
Option Provider Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.options.providers.provider_factory import OptionProviderFactory


def main():

    provider = OptionProviderFactory.create()

    print("=" * 80)
    print("OPTION PROVIDER")
    print("=" * 80)
    print(type(provider).__name__)
    print("=" * 80)


if __name__ == "__main__":
    main()