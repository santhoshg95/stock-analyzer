"""
Portfolio Optimizer

Optimizes capital allocation using confidence,
risk management and Kelly Criterion.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class PortfolioPosition:

    symbol: str

    confidence: float

    expected_return: float

    volatility: float

    weight: float

    allocation: float

    shares: int


class PortfolioOptimizer:

    def __init__(

        self,

        capital: float,

        max_position_size: float = 0.10,

        max_risk_per_trade: float = 0.02,

    ):

        self.capital = capital

        self.max_position_size = max_position_size

        self.max_risk_per_trade = max_risk_per_trade

    # ---------------------------------------------------------

    def optimize(

        self,

        opportunities: List[Dict[str, Any]],

    ) -> List[PortfolioPosition]:

        if not opportunities:

            return []

        weights = []

        for trade in opportunities:

            weight = self.position_weight(trade)

            weights.append(weight)

        total = sum(weights)

        if total <= 0:

            return []

        portfolio = []

        for trade, weight in zip(

            opportunities,

            weights,

        ):

            normalized = weight / total

            normalized = min(

                normalized,

                self.max_position_size,

            )

            allocation = normalized * self.capital

            price = trade.get("price", 1)

            shares = int(

                allocation / price

            )

            portfolio.append(

                PortfolioPosition(

                    symbol=trade["symbol"],

                    confidence=trade["confidence"],

                    expected_return=trade["expected_return"],

                    volatility=trade["volatility"],

                    weight=round(

                        normalized,

                        4,

                    ),

                    allocation=round(

                        allocation,

                        2,

                    ),

                    shares=max(

                        shares,

                        0,

                    ),

                )

            )

        return portfolio

    # ---------------------------------------------------------

    def position_weight(

        self,

        trade: Dict[str, Any],

    ) -> float:

        confidence = trade.get(

            "confidence",

            50,

        )

        expected = trade.get(

            "expected_return",

            0,

        )

        volatility = max(

            trade.get(

                "volatility",

                0.30,

            ),

            0.01,

        )

        kelly = self.kelly_fraction(

            confidence,

            expected,

        )

        return (

            confidence

            * expected

            * kelly

        ) / volatility

    # ---------------------------------------------------------

    @staticmethod

    def kelly_fraction(

        confidence: float,

        expected_return: float,

    ) -> float:

        probability = confidence / 100

        reward = max(

            expected_return,

            0.01,

        )

        risk = 1.0

        kelly = (

            probability * reward

            - (1 - probability)

        ) / risk

        return max(

            0.0,

            min(

                kelly,

                1.0,

            ),

        )

    # ---------------------------------------------------------

    def total_allocation(

        self,

        portfolio: List[PortfolioPosition],

    ) -> float:

        return round(

            sum(

                p.allocation

                for p in portfolio

            ),

            2,

        )

    # ---------------------------------------------------------

    @staticmethod

    def expected_portfolio_return(

        portfolio: List[PortfolioPosition],

    ) -> float:

        if not portfolio:

            return 0.0

        return round(

            sum(

                p.expected_return

                * p.weight

                for p in portfolio

            ),

            4,

        )

    # ---------------------------------------------------------

    @staticmethod

    def average_confidence(

        portfolio: List[PortfolioPosition],

    ) -> float:

        if not portfolio:

            return 0.0

        return round(

            sum(

                p.confidence

                for p in portfolio

            )

            / len(portfolio),

            2,

        )

    # ---------------------------------------------------------

    @staticmethod

    def summary(

        portfolio: List[PortfolioPosition],

    ) -> Dict[str, Any]:

        return {

            "positions": len(portfolio),

            "expected_return":

                PortfolioOptimizer.expected_portfolio_return(

                    portfolio,

                ),

            "average_confidence":

                PortfolioOptimizer.average_confidence(

                    portfolio,

                ),

            "allocation":

                round(

                    sum(

                        p.allocation

                        for p in portfolio

                    ),

                    2,

                ),

        }

    # ---------------------------------------------------------

    @staticmethod

    def export(

        portfolio: List[PortfolioPosition],

    ) -> List[Dict[str, Any]]:

        return [

            asdict(position)

            for position in portfolio

        ]