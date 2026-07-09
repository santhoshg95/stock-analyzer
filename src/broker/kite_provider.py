"""
Kite Provider

Thin wrapper around Kite Connect.
"""

from src.broker.kite_auth import KiteAuthentication


class KiteProvider:

    def __init__(self):

        auth = KiteAuthentication()

        self.kite = auth.get_client()

    # --------------------------------------

    def get_ltp(self, symbol):

        exchange_symbol = f"NSE:{symbol}"

        response = self.kite.ltp([exchange_symbol])

        data = response[exchange_symbol]

        return {

            "symbol": symbol,

            "ltp": data["last_price"]

        }

    # --------------------------------------

    def get_ltps(self, symbols):

        exchange_symbols = [

            f"NSE:{symbol}"

            for symbol in symbols

        ]

        response = self.kite.ltp(exchange_symbols)

        result = {}

        for item in exchange_symbols:

            symbol = item.split(":")[1]

            result[symbol] = {

                "symbol": symbol,

                "ltp": response[item]["last_price"]

            }

        return result