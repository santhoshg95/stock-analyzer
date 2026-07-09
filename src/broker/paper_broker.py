"""
Paper Trading Broker

Simulates a broker.
"""

from src.broker.base_broker import BaseBroker


class PaperBroker(BaseBroker):

    def __init__(self):

        self.orders = []

    def connect(self):

        print("Paper Broker Connected")

    def get_ltp(self, symbol):

        print(f"Fetching LTP for {symbol}")

        return None

    def place_order(

        self,

        symbol,

        transaction_type,

        quantity,

        order_type="MARKET",

        price=None,

    ):

        order = {

            "symbol": symbol,

            "transaction_type": transaction_type,

            "quantity": quantity,

            "order_type": order_type,

            "price": price,

            "status": "FILLED"

        }

        self.orders.append(order)

        print("Paper Order Executed")

        return order

    def positions(self):

        return self.orders

    def holdings(self):

        return []