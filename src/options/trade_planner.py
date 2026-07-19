"""
Trade Planner

Builds executable option trade plans from
strategy selection and strike optimization.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

from .strategy_selector import (
    OptionsStrategySelector,
)

from .strike_optimizer import (
    StrikeOptimizer,
)


@dataclass
class TradePlan:

    symbol: str

    strategy: str

    action: str

    expiry: str

    strike: float

    option_type: str

    premium: float

    quantity: int

    estimated_credit: float

    probability_of_profit: float

    expected_return: float

    risk_reward: float

    confidence: float

    notes: list[str]


class TradePlanner:

    DEFAULT_LOT_SIZE = 1

    def __init__(

        self,

        selector: Optional[
            OptionsStrategySelector
        ] = None,

        optimizer: Optional[
            StrikeOptimizer
        ] = None,

    ):

        self.selector = (

            selector

            or OptionsStrategySelector()

        )

        self.optimizer = (

            optimizer

            or StrikeOptimizer()

        )

    # ----------------------------------------------------

    def build(

        self,

        symbol: str,

        option_chain: Dict[str, Any],

        option_contracts: list,

        period: str = "10y",

        quantity: int = DEFAULT_LOT_SIZE,

    ) -> TradePlan:

        selected = self.selector.select(

            symbol,

            option_chain,

            period,

        )

        optimized = self.optimizer.optimize(

            selected.strategy,

            option_contracts,

        )

        action = self._action(

            selected.strategy

        )

        credit = (

            optimized.premium

            * quantity

        )

        notes = [

            f"Expected Market: {selected.expected_market}",

            f"Risk Level: {selected.risk_level}",

            f"Strategy Confidence: {selected.confidence:.2f}%",

            f"Selected using delta optimization",

        ]

        return TradePlan(

            symbol=symbol,

            strategy=selected.strategy,

            action=action,

            expiry=optimized.expiry,

            strike=optimized.strike,

            option_type=optimized.option_type,

            premium=optimized.premium,

            quantity=quantity,

            estimated_credit=round(

                credit,

                2,

            ),

            probability_of_profit=optimized.probability_of_profit,

            expected_return=optimized.expected_return,

            risk_reward=optimized.risk_reward,

            confidence=optimized.score,

            notes=notes,

        )

    # ----------------------------------------------------

    @staticmethod

    def _action(

        strategy: str,

    ) -> str:

        sell_strategies = {

            "Covered Call",

            "Cash Secured Put",

            "Iron Condor",

            "Iron Butterfly",

            "Bull Put Spread",

            "Bear Call Spread",

        }

        if strategy in sell_strategies:

            return "SELL"

        return "BUY"

    # ----------------------------------------------------

    @staticmethod

    def as_dict(

        trade: TradePlan,

    ) -> Dict[str, Any]:

        return asdict(trade)