"""
Quote Service

Provides live market quotes using Zerodha.

Supports:

- Single Quote
- Multiple Quotes
- In-memory cache
"""

from src.broker.kite_provider import KiteProvider
from src.services.quote_cache import QuoteCache


class QuoteService:

    def __init__(self):

        self.provider = KiteProvider()

        self.cache = QuoteCache()

    # --------------------------------------

    def get_quote(self, symbol):

        cached = self.cache.get(symbol)

        if cached:

            return cached

        quote = self.provider.get_ltp(symbol)

        self.cache.put(symbol, quote)

        return quote

    # --------------------------------------

    def get_quotes(self, symbols):

        quotes = {}

        missing = []

        for symbol in symbols:

            cached = self.cache.get(symbol)

            if cached:

                quotes[symbol] = cached

            else:

                missing.append(symbol)

        if missing:

            live_quotes = self.provider.get_ltps(missing)

            for symbol, quote in live_quotes.items():

                self.cache.put(symbol, quote)

                quotes[symbol] = quote

        return quotes

    # --------------------------------------

    def clear_cache(self):

        self.cache.clear()