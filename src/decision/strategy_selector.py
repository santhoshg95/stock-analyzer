"""
Strategy Selector
"""

from src.models.strategy import Strategy


class StrategySelector:

    @staticmethod
    def bullish():

        return [

            Strategy(

                "Bull Put Spread",

                "BULLISH",

                "Collect premium while expecting price to stay above support."

            ),

            Strategy(

                "Cash Secured Put",

                "BULLISH",

                "Sell put with cash reserved."

            )

        ]

    @staticmethod
    def bearish():

        return [

            Strategy(

                "Bear Call Spread",

                "BEARISH",

                "Collect premium while expecting resistance to hold."

            ),

            Strategy(

                "Bear Put Spread",

                "BEARISH",

                "Directional bearish debit spread."

            )

        ]

    @staticmethod
    def sideways():

        return [

            Strategy(

                "Iron Condor",

                "SIDEWAYS",

                "Sell premium when expecting a range-bound market."

            ),

            Strategy(

                "Iron Butterfly",

                "SIDEWAYS",

                "Neutral premium selling strategy."

            )

        ]