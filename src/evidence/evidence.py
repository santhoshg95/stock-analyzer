"""
Evidence Model

Represents one piece of evidence used by the AI.
"""

from dataclasses import dataclass


@dataclass
class Evidence:

    source: str

    title: str

    score: float

    confidence: float

    description: str