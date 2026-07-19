"""Build a live equity option chain from Zerodha Kite quotes."""

from __future__ import annotations

from datetime import date

from src.options.models.option_chain import OptionChain
from src.options.models.option_contract import OptionContract


class KiteOptionChainProvider:
    """Loads the nearest expiry's contracts and quote/OI data from Kite."""

    def __init__(self, kite):
        self.kite = kite

    def get_chain(self, symbol: str, spot_price: float, width: float = 0.15) -> OptionChain:
        symbol = symbol.upper()
        today = date.today()
        instruments = [
            item for item in self.kite.instruments("NFO")
            if item.get("name", "").upper() == symbol
            and item.get("instrument_type") in {"CE", "PE"}
            and item.get("expiry")
            and item["expiry"] >= today
        ]
        if not instruments:
            raise ValueError(f"No live option contracts found for {symbol}")
        expiry = min(item["expiry"] for item in instruments)
        minimum, maximum = spot_price * (1 - width), spot_price * (1 + width)
        contracts = [
            item for item in instruments
            if item["expiry"] == expiry and minimum <= float(item["strike"]) <= maximum
        ]
        quote_symbols = [f"NFO:{item['tradingsymbol']}" for item in contracts]
        quotes = {}
        for offset in range(0, len(quote_symbols), 200):
            quotes.update(self.kite.quote(quote_symbols[offset:offset + 200]))

        calls, puts = [], []
        for item in contracts:
            quote = quotes.get(f"NFO:{item['tradingsymbol']}", {})
            depth = quote.get("depth", {})
            buy, sell = depth.get("buy", []), depth.get("sell", [])
            contract = OptionContract(
                symbol=item["tradingsymbol"], expiry=str(expiry), strike=float(item["strike"]),
                option_type=item["instrument_type"], last_price=float(quote.get("last_price") or 0),
                bid=float(buy[0]["price"]) if buy else 0.0,
                ask=float(sell[0]["price"]) if sell else 0.0,
                volume=int(quote.get("volume") or 0), open_interest=int(quote.get("oi") or 0),
                change_in_oi=int(quote.get("oi_day_high") or 0), implied_volatility=0.0,
            )
            (calls if contract.option_type == "CE" else puts).append(contract)
        return OptionChain(symbol=symbol, spot_price=spot_price, expiry=str(expiry), calls=calls, puts=puts)
