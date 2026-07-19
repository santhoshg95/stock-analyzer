"""
Earnings Rule

Placeholder implementation.
"""

from src.rules.base_rule import BaseRule
from src.rules.rule_result import RuleResult


class EarningsRule(BaseRule):

    def evaluate(self, context):

        return RuleResult(

            name="EARNINGS",

            passed=True,

            severity="INFO",

            reason="Earnings calendar not integrated yet."

        )