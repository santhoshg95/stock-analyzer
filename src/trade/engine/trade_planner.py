"""
Trade Planner

Creates an executable trade plan from the selected strategy.
"""

from src.context.stock_context import StockContext

from src.trade.models.trade_plan import TradePlan


class TradePlanner:
    """
    Converts strategy into a trade plan.
    """

    DEFAULT_CAPITAL = 100000

    RISK_PERCENT = 1.0

    def create_plan(
        self,
        context: StockContext,
    ) -> TradePlan:

        if context.strategy is None:

            raise ValueError(
                "Strategy is required before creating a trade plan."
            )

        market_price = context.market.last_price

        stop_loss = round(
            market_price * 0.98,
            2,
        )

        risk_per_share = market_price - stop_loss

        capital = self.DEFAULT_CAPITAL

        max_risk = capital * (self.RISK_PERCENT / 100)

        quantity = int(max_risk / risk_per_share)

        quantity = max(quantity, 1)

        capital_required = round(
            quantity * market_price,
            2,
        )

        target1 = round(
            market_price + risk_per_share * 2,
            2,
        )

        target2 = round(
            market_price + risk_per_share * 3,
            2,
        )

        target3 = round(
            market_price + risk_per_share * 5,
            2,
        )

        expected_profit = round(
            (target2 - market_price) * quantity,
            2,
        )

        maximum_loss = round(
            risk_per_share * quantity,
            2,
        )

        return TradePlan(

            symbol=context.symbol,

            strategy=context.strategy.name,

            action=context.decision.action,

            entry_price=market_price,

            stop_loss=stop_loss,

            target_1=target1,

            target_2=target2,

            target_3=target3,

            quantity=quantity,

            capital_required=capital_required,

            risk_reward_ratio=3.0,

            maximum_loss=maximum_loss,

            expected_profit=expected_profit,

            trailing_stop=True,

            holding_period=context.strategy.expected_holding_period,

            reasons=context.strategy.reasons,
        )