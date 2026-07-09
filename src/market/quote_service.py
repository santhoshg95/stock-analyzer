"""
Live Quote Service

Downloads quotes in batches.
"""

from math import ceil


class QuoteService:

    def __init__(self, kite):

        self.kite = kite

    # ----------------------------------------------------

    def get_quotes(

        self,

        symbols,

        batch_size=200

    ):

        all_quotes = {}

        total_batches = ceil(len(symbols) / batch_size)

        for batch_no in range(total_batches):

            start = batch_no * batch_size

            end = start + batch_size

            batch = symbols[start:end]

            print(

                f"Batch {batch_no + 1}/{total_batches} "

                f"({len(batch)} symbols)"

            )

            quotes = self.kite.quote(batch)

            all_quotes.update(quotes)

        return all_quotes