"""
Option Models Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.options.models.option_contract import OptionContract
from src.options.models.option_chain import OptionChain
from src.options.models.option_analysis import OptionAnalysis


def main():

    contract = OptionContract(

        symbol="SBIN",

        expiry="31-Jul-2026",

        strike=1000,

        option_type="PE",

        last_price=18.50,

        bid=18.45,

        ask=18.55,

        volume=15000,

        open_interest=250000,

        change_in_oi=12000,

        implied_volatility=18.4

    )

    chain = OptionChain(

        symbol="SBIN",

        spot_price=1022.40,

        expiry="31-Jul-2026",

        puts=[contract],

        calls=[]

    )

    analysis = OptionAnalysis(

        status="BULLISH",

        confidence=90,

        score=92,

        pcr=1.28,

        max_pain=1000,

        iv_rank=65,

        strongest_support=1000,

        strongest_resistance=1050,

        suggested_strategy="Bull Put Spread",

        reasons=[

            "Strong Put Writing",

            "PCR above 1",

            "Healthy IV"

        ]

    )

    print("=" * 100)
    print("OPTION MODELS")
    print("=" * 100)

    print(chain)

    print()

    print(analysis)

    print("=" * 100)


if __name__ == "__main__":
    main()