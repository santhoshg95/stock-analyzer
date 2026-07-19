"""
Option Engine Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.options.engine.option_engine import OptionEngine
from src.options.models.option_chain import OptionChain
from src.options.models.option_contract import OptionContract


def create_contract(
    strike,
    option_type,
    oi,
    volume,
    bid,
    ask,
    iv,
):

    return OptionContract(

        symbol="SBIN",

        expiry="31-Jul-2026",

        strike=strike,

        option_type=option_type,

        last_price=(bid + ask) / 2,

        bid=bid,

        ask=ask,

        volume=volume,

        open_interest=oi,

        change_in_oi=5000,

        implied_volatility=iv

    )


def main():

    calls = [

        create_contract(
            1050,
            "CE",
            250000,
            5000,
            10,
            10.1,
            28
        ),

        create_contract(
            1060,
            "CE",
            800,
            20,
            5,
            6.5,
            30
        )

    ]

    puts = [

        create_contract(
            1000,
            "PE",
            400000,
            7000,
            12,
            12.1,
            29
        ),

        create_contract(
            990,
            "PE",
            700,
            10,
            3,
            5.2,
            27
        )

    ]

    chain = OptionChain(

        symbol="SBIN",

        spot_price=1022,

        expiry="31-Jul-2026",

        calls=calls,

        puts=puts

    )

    engine = OptionEngine()

    analysis = engine.analyze(chain)

    print("=" * 100)
    print("OPTION ENGINE")
    print("=" * 100)

    print(f"Status        : {analysis.status}")
    print(f"Confidence    : {analysis.confidence}")
    print(f"PCR           : {analysis.pcr}")
    print(f"Average IV    : {analysis.iv_rank}")
    print(f"Max Pain      : {analysis.max_pain}")
    print(f"Support       : {analysis.strongest_support}")
    print(f"Resistance    : {analysis.strongest_resistance}")

    print("\nReasons")

    for reason in analysis.reasons:
        print(f"• {reason}")

    print("=" * 100)


if __name__ == "__main__":
    main()