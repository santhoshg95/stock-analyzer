"""
Paper Trading Broker

Simulates a broker.
"""

from datetime import datetime, timezone
from uuid import uuid4

from src.broker.base_broker import BaseBroker


class PaperBroker(BaseBroker):

    def __init__(self, starting_cash=100000.0):
        if starting_cash <= 0:
            raise ValueError("starting_cash must be positive")
        self.starting_cash = float(starting_cash)
        self.cash = float(starting_cash)
        self.orders = []
        self._positions = {}

    def connect(self):

        return True

    def get_ltp(self, symbol):

        return None

    def place_order(

        self,

        symbol,

        transaction_type,

        quantity,

        order_type="MARKET",

        price=None,

    ):

        side = str(transaction_type).upper()
        if side not in {"BUY", "SELL"}:
            raise ValueError("transaction_type must be BUY or SELL")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer")
        if price is None or price <= 0:
            raise ValueError("paper orders require a positive execution price")

        position = self._positions.get(symbol, {"quantity": 0, "average_price": 0.0})
        value = round(quantity * float(price), 2)
        if side == "BUY":
            if value > self.cash:
                raise ValueError("insufficient paper cash")
            new_quantity = position["quantity"] + quantity
            position["average_price"] = round(
                ((position["quantity"] * position["average_price"]) + value) / new_quantity, 2
            )
            position["quantity"] = new_quantity
            self.cash -= value
        else:
            if quantity > position["quantity"]:
                raise ValueError("cannot sell more shares than the paper position")
            position["quantity"] -= quantity
            self.cash += value

        if position["quantity"]:
            self._positions[symbol] = position
        else:
            self._positions.pop(symbol, None)

        order = {

            "order_id": str(uuid4()),

            "symbol": symbol,

            "transaction_type": transaction_type,

            "quantity": quantity,

            "order_type": order_type,

            "price": price,

            "status": "FILLED",
            "filled_price": round(float(price), 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),

        }

        self.orders.append(order)

        return order

    def positions(self):

        return [
            {"symbol": symbol, **position}
            for symbol, position in sorted(self._positions.items())
        ]

    def holdings(self):

        return self.positions()

    def portfolio(self):
        invested = sum(position["quantity"] * position["average_price"] for position in self._positions.values())
        return {
            "starting_cash": round(self.starting_cash, 2),
            "cash": round(self.cash, 2),
            "invested_cost": round(invested, 2),
            "positions": self.positions(),
            "orders": self.orders,
        }
