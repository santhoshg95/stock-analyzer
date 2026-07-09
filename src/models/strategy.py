"""
Strategy Model
"""

from dataclasses import dataclass


@dataclass
class Strategy:

    name: str

    direction: str

    description: str