"""
Broker Factory
"""

from src.broker.paper_broker import PaperBroker


class BrokerFactory:

    @staticmethod
    def create(name):

        if name.lower() == "paper":

            return PaperBroker()

        raise ValueError(

            f"Unknown broker : {name}"

        )