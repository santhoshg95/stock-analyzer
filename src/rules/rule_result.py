"""
Rule Result

Represents the output of a trading rule.
"""

from dataclasses import dataclass


@dataclass
class RuleResult:

    name: str

    passed: bool

    severity: str

    reason: str