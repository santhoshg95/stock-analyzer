"""
Rule Engine

Runs all trading rules.
"""

from src.rules.market_rule import MarketRule
from src.rules.volatility_rule import VolatilityRule
from src.rules.liquidity_rule import LiquidityRule
from src.rules.earnings_rule import EarningsRule


class RuleEngine:

    def __init__(self):

        self.rules = [

            MarketRule(),

            VolatilityRule(),

            LiquidityRule(),

            EarningsRule()

        ]

    def evaluate(self, context):

        results = []

        overall = True

        for rule in self.rules:

            result = rule.evaluate(context)

            results.append(result)

            if not result.passed:

                overall = False

        return {

            "passed": overall,

            "results": results

        }