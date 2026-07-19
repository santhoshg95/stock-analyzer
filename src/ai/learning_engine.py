"""
Learning Engine

Tracks completed trades and continuously measures
strategy performance.

Author:
    AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Any


@dataclass
class TradeRecord:

    symbol: str

    strategy: str

    recommendation: str

    predicted_confidence: float

    actual_return: float

    successful: bool

    holding_days: int


class LearningEngine:

    def __init__(self):

        self.records: List[TradeRecord] = []

    # ---------------------------------------------------------

    def record_trade(

        self,

        trade: TradeRecord,

    ) -> None:

        self.records.append(trade)

    # ---------------------------------------------------------

    def total_trades(self) -> int:

        return len(self.records)

    # ---------------------------------------------------------

    def win_rate(self) -> float:

        if not self.records:

            return 0.0

        wins = sum(

            trade.successful

            for trade in self.records

        )

        return round(

            wins

            / len(self.records)

            * 100,

            2,

        )

    # ---------------------------------------------------------

    def average_return(self) -> float:

        if not self.records:

            return 0.0

        return round(

            sum(

                trade.actual_return

                for trade in self.records

            )

            / len(self.records),

            2,

        )

    # ---------------------------------------------------------

    def average_holding_period(self) -> float:

        if not self.records:

            return 0.0

        return round(

            sum(

                trade.holding_days

                for trade in self.records

            )

            / len(self.records),

            2,

        )

    # ---------------------------------------------------------

    def strategy_statistics(self) -> Dict[str, Dict]:

        statistics = {}

        for trade in self.records:

            strategy = trade.strategy

            if strategy not in statistics:

                statistics[strategy] = {

                    "trades": 0,

                    "wins": 0,

                    "losses": 0,

                    "total_return": 0.0,

                }

            statistics[strategy]["trades"] += 1

            if trade.successful:

                statistics[strategy]["wins"] += 1

            else:

                statistics[strategy]["losses"] += 1

            statistics[strategy]["total_return"] += (

                trade.actual_return

            )

        for strategy in statistics.values():

            trades = strategy["trades"]

            strategy["win_rate"] = round(

                strategy["wins"]

                / trades

                * 100,

                2,

            )

            strategy["average_return"] = round(

                strategy["total_return"]

                / trades,

                2,

            )

        return statistics

    # ---------------------------------------------------------

    def prediction_accuracy(self) -> float:

        if not self.records:

            return 0.0

        score = 0.0

        for trade in self.records:

            expected = trade.predicted_confidence / 100

            actual = 1 if trade.successful else 0

            score += 1 - abs(

                expected - actual

            )

        return round(

            score

            / len(self.records)

            * 100,

            2,

        )

    # ---------------------------------------------------------

    def best_strategy(self) -> Dict[str, Any]:

        stats = self.strategy_statistics()

        if not stats:

            return {}

        best = max(

            stats.items(),

            key=lambda item: (

                item[1]["win_rate"],

                item[1]["average_return"],

            ),

        )

        return {

            "strategy": best[0],

            **best[1],

        }

    # ---------------------------------------------------------

    def worst_strategy(self) -> Dict[str, Any]:

        stats = self.strategy_statistics()

        if not stats:

            return {}

        worst = min(

            stats.items(),

            key=lambda item: (

                item[1]["win_rate"],

                item[1]["average_return"],

            ),

        )

        return {

            "strategy": worst[0],

            **worst[1],

        }

    # ---------------------------------------------------------

    def summary(self) -> Dict[str, Any]:

        return {

            "total_trades": self.total_trades(),

            "win_rate": self.win_rate(),

            "average_return": self.average_return(),

            "average_holding_period": self.average_holding_period(),

            "prediction_accuracy": self.prediction_accuracy(),

            "best_strategy": self.best_strategy(),

            "worst_strategy": self.worst_strategy(),

        }

    # ---------------------------------------------------------

    def export_records(self) -> List[Dict[str, Any]]:

        return [

            asdict(record)

            for record in self.records

        ]

    # ---------------------------------------------------------

    def clear(self) -> None:

        self.records.clear()