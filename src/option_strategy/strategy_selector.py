"""
Strategy Selector
"""

from src.models.option_strategy import OptionStrategy


class StrategySelector:

    @staticmethod
    def bullish():

        return [

            OptionStrategy(

                name="Bull Put Spread",

                market_bias="BULLISH",

                volatility="MEDIUM",

                description="Sell OTM Put and buy lower strike Put."

            ),

            OptionStrategy(

                name="Cash Secured Put",

                market_bias="BULLISH",

                volatility="LOW",

                description="Sell Put while keeping cash ready."

            )

        ]

    @staticmethod

    def bearish():

        return [

            OptionStrategy(

                name="Bear Call Spread",

                market_bias="BEARISH",

                volatility="MEDIUM",

                description="Sell OTM Call and buy higher strike Call."

            )

        ]

    @staticmethod

    def sideways():

        return [

            OptionStrategy(

                name="Iron Condor",

                market_bias="SIDEWAYS",

                volatility="LOW",

                description="Premium selling in a range-bound market."

            ),

            OptionStrategy(

                name="Iron Butterfly",

                market_bias="SIDEWAYS",

                volatility="LOW",

                description="Neutral premium selling."

            )

        ]