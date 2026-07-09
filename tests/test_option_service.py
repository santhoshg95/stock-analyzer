"""
Option Service Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.option_chain.option_service import OptionChainService


def main():

    service = OptionChainService()

    print("=" * 90)

    print("OPTION SERVICE")

    print("=" * 90)

    try:

        service.get_option_chain(

            "NIFTY"

        )

    except NotImplementedError as ex:

        print(ex)

    print("=" * 90)


if __name__ == "__main__":

    main()