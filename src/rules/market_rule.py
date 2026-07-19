"""
Market Rule
"""

from src.rules.base_rule import BaseRule
from src.rules.rule_result import RuleResult


class MarketRule(BaseRule):

    def evaluate(self, context):

        market = context.market

        if market.status == "BEARISH":

            return RuleResult(

                name="MARKET",

                passed=False,

                severity="HIGH",

                reason="Overall market regime is bearish."

            )

        return RuleResult(

            name="MARKET",

            passed=True,

            severity="INFO",

            reason="Market conditions are acceptable."

        )