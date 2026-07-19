"""
Liquidity Rule

Placeholder implementation.
"""

from src.rules.base_rule import BaseRule
from src.rules.rule_result import RuleResult


class LiquidityRule(BaseRule):

    def evaluate(self, context):

        return RuleResult(

            name="LIQUIDITY",

            passed=True,

            severity="INFO",

            reason="Liquidity rule not yet connected."

        )