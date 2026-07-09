"""
Decision Model
"""

from dataclasses import dataclass


@dataclass
class Decision:

    action: str

    confidence: int

    reason: str