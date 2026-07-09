"""
Paper Broker Test
"""

import os
import sys

PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.broker.broker_factory import BrokerFactory


def main():

    broker = BrokerFactory.create("paper")

    broker.connect()

    broker.place_order(

        symbol="RELIANCE",

        transaction_type="BUY",

        quantity=10

    )

    print()

    print("=" * 90)

    print("POSITIONS")

    print("=" * 90)

    for position in broker.positions():

        print(position)


if __name__ == "__main__":

    main()