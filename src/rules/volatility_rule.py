"""
Volatility Rule

Placeholder implementation.
"""

from src.rules.base_rule import BaseRule
from src.rules.rule_result import RuleResult


class VolatilityRule(BaseRule):

    def evaluate(self, context):

        return RuleResult(

            name="VOLATILITY",

            passed=True,

            severity="INFO",

            reason="Volatility rule not yet connected."

        )