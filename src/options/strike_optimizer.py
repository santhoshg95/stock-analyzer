"""
Strike Optimizer

Selects the optimal option contract for the chosen strategy.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, List


@dataclass
class OptimizedStrike:

    strategy: str

    expiry: str

    strike: float

    option_type: str

    delta: float

    premium: float

    probability_of_profit: float

    risk_reward: float

    expected_return: float

    score: float


class StrikeOptimizer:

    DELTA_TARGETS = {

        "Covered Call": 0.30,

        "Cash Secured Put": -0.30,

        "Bull Put Spread": -0.25,

        "Bear Call Spread": 0.25,

        "Iron Condor": 0.15,

        "Iron Butterfly": 0.10,

        "Calendar Spread": 0.50,

        "Diagonal Spread": 0.40,

    }

    # -----------------------------------------------------

    def optimize(

        self,

        strategy: str,

        option_chain: List[Dict[str, Any]],

    ) -> OptimizedStrike:

        if not option_chain:

            raise ValueError(
                "Option chain is empty."
            )

        target = self.DELTA_TARGETS.get(

            strategy,

            0.30,

        )

        best = None

        best_score = -1.0

        for option in option_chain:

            score = self.score_option(

                option,

                target,

            )

            if score > best_score:

                best = option

                best_score = score

        return OptimizedStrike(

            strategy=strategy,

            expiry=best["expiry"],

            strike=best["strike"],

            option_type=best["type"],

            delta=best["delta"],

            premium=best["premium"],

            probability_of_profit=self.pop(best),

            risk_reward=self.risk_reward(best),

            expected_return=self.expected_return(best),

            score=round(best_score, 2),

        )

    # -----------------------------------------------------

    @staticmethod

    def score_option(

        option: Dict[str, Any],

        target_delta: float,

    ) -> float:

        delta_score = (

            100

            - abs(

                abs(option["delta"])

                - abs(target_delta)

            )

            * 100

        )

        iv_score = option.get(

            "iv_rank",

            50,

        )

        oi_score = min(

            option.get(

                "open_interest",

                0,

            )

            / 1000,

            100,

        )

        spread = option.get(

            "bid_ask_spread",

            1,

        )

        spread_score = max(

            0,

            100

            - spread * 200,

        )

        return (

            delta_score * 0.40

            +

            iv_score * 0.20

            +

            oi_score * 0.20

            +

            spread_score * 0.20

        )

    # -----------------------------------------------------

    @staticmethod

    def pop(

        option: Dict[str, Any],

    ) -> float:

        delta = abs(

            option["delta"]

        )

        return round(

            (1 - delta)

            * 100,

            2,

        )

    # -----------------------------------------------------

    @staticmethod

    def risk_reward(

        option: Dict[str, Any],

    ) -> float:

        premium = option.get(

            "premium",

            1,

        )

        risk = option.get(

            "max_loss",

            premium * 10,

        )

        if risk <= 0:

            return 0.0

        return round(

            premium / risk,

            2,

        )

    # -----------------------------------------------------

    @staticmethod

    def expected_return(

        option: Dict[str, Any],

    ) -> float:

        premium = option.get(

            "premium",

            0,

        )

        pop = StrikeOptimizer.pop(

            option

        ) / 100

        return round(

            premium * pop,

            2,

        )

    # -----------------------------------------------------

    @staticmethod

    def as_dict(

        optimized: OptimizedStrike,

    ) -> Dict[str, Any]:

        return asdict(

            optimized

        )