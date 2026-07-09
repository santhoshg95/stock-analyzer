"""
Quote Cache

Stores live quotes in memory.

Every engine should read quotes from here instead of
calling Zerodha directly.
"""


class QuoteCache:

    def __init__(self):

        self.cache = {}

    def put(self, symbol, quote):

        self.cache[symbol] = quote

    def get(self, symbol):

        return self.cache.get(symbol)

    def get_all(self):

        return self.cache

    def clear(self):

        self.cache.clear()