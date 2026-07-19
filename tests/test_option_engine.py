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


def contract(
    strike,
    option_type,
    oi,
    volume,
    bid,
    ask,
    iv,
    delta,
    gamma,
    theta,
    vega,
    rho,
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

        implied_volatility=iv,

        delta=delta,

        gamma=gamma,

        theta=theta,

        vega=vega,

        rho=rho,

    )


def main():

    calls = [

        contract(
            1050,
            "CE",
            250000,
            5000,
            10,
            10.1,
            28,
            0.45,
            0.05,
            -2.1,
            0.18,
            0.07,
        ),

        contract(
            1060,
            "CE",
            800,
            20,
            5,
            6.5,
            30,
            0.35,
            0.03,
            -1.8,
            0.16,
            0.05,
        ),

    ]

    puts = [

        contract(
            1000,
            "PE",
            400000,
            7000,
            12,
            12.1,
            29,
            -0.42,
            0.06,
            -2.4,
            0.19,
            -0.04,
        ),

        contract(
            990,
            "PE",
            700,
            10,
            3,
            5.2,
            27,
            -0.50,
            0.08,
            -2.8,
            0.22,
            -0.06,
        ),

    ]

    chain = OptionChain(

        symbol="SBIN",

        spot_price=1022,

        expiry="31-Jul-2026",

        calls=calls,

        puts=puts,

    )

    engine = OptionEngine()

    analysis = engine.analyze(chain)

    print("=" * 100)
    print("OPTION ENGINE")
    print("=" * 100)

    print(f"Status        : {analysis.status}")
    print(f"Confidence    : {analysis.confidence}")
    print(f"Score         : {analysis.score}")
    print(f"PCR           : {analysis.pcr}")
    print(f"Average IV    : {analysis.iv_rank}")
    print(f"Max Pain      : {analysis.max_pain}")
    print(f"Support       : {analysis.strongest_support}")
    print(f"Resistance    : {analysis.strongest_resistance}")
    print(f"Strategy      : {analysis.suggested_strategy}")

    print("\nReasons")

    for reason in analysis.reasons:

        print(f"• {reason}")

    print("=" * 100)


if __name__ == "__main__":
    main()