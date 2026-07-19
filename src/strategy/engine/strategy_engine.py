"""
Strategy Engine

Converts AI Decision into an executable trading strategy.
"""

from src.context.stock_context import StockContext

from src.strategy.models.trading_strategy import TradingStrategy


class StrategyEngine:
    """
    Determines the most appropriate execution strategy.
    """

    def select(
        self,
        context: StockContext,
    ) -> TradingStrategy:

        if context.decision is None:

            return TradingStrategy(

                name="NO_STRATEGY",

                asset_type="NONE",

                direction="NONE",

                confidence=0,

                expected_holding_period="NONE",

                reasons=[
                    "Decision is not available."
                ],
            )

        decision = context.decision

        # ----------------------------------------------------
        # BUY
        # ----------------------------------------------------

        if decision.action in ("BUY", "STRONG_BUY"):

            # Option intelligence available

            if (
                context.options
                and context.options.analysis
                and context.options.analysis.suggested_strategy
            ):

                return TradingStrategy(

                    name=context.options.analysis.suggested_strategy,

                    asset_type="OPTIONS",

                    direction="LONG",

                    confidence=decision.confidence,

                    expected_holding_period="3-10 Days",

                    reasons=decision.reasons,

                )

            # Default equity strategy

            return TradingStrategy(

                name="Cash Equity",

                asset_type="EQUITY",

                direction="LONG",

                confidence=decision.confidence,

                expected_holding_period="3-10 Days",

                reasons=decision.reasons,

            )

        # ----------------------------------------------------
        # SELL
        # ----------------------------------------------------

        if decision.action in ("SELL", "STRONG_SELL"):

            return TradingStrategy(

                name="Short Futures",

                asset_type="FUTURES",

                direction="SHORT",

                confidence=decision.confidence,

                expected_holding_period="1-5 Days",

                reasons=decision.reasons,

            )

        # ----------------------------------------------------
        # HOLD
        # ----------------------------------------------------

        return TradingStrategy(

            name="Wait",

            asset_type="NONE",

            direction="NEUTRAL",

            confidence=decision.confidence,

            expected_holding_period="N/A",

            reasons=decision.reasons,

        )