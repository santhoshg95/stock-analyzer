"""
Option Strategy Engine

Determines which option selling strategies
are suitable based on the analysis pipeline.
"""

from src.models.strategy_report import StrategyReport
from src.option_strategy.strategy_selector import StrategySelector


class OptionStrategyEngine:

    def recommend(self, analysis):

        market = analysis.market.status

        if market == "BULLISH":

            return StrategyReport(

                symbol=analysis.symbol,

                recommended=StrategySelector.bullish(),

                rejected=StrategySelector.bearish()
                + StrategySelector.sideways(),

                reason="Overall market regime is bullish."

            )

        if market == "BEARISH":

            return StrategyReport(

                symbol=analysis.symbol,

                recommended=StrategySelector.bearish(),

                rejected=StrategySelector.bullish()
                + StrategySelector.sideways(),

                reason="Overall market regime is bearish."

            )

        return StrategyReport(

            symbol=analysis.symbol,

            recommended=StrategySelector.sideways(),

            rejected=StrategySelector.bullish()
            + StrategySelector.bearish(),

            reason="Market is neutral or uncertain."

        )