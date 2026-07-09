"""
Complete Analysis Result

Contains the output from all analysis engines.
"""

from dataclasses import dataclass
from typing import Optional

from src.models.decision_context import DecisionContext


@dataclass
class AnalysisResult:

    symbol: str

    market: Optional[DecisionContext] = None

    sector: Optional[DecisionContext] = None

    technical: Optional[DecisionContext] = None

    breakout: Optional[DecisionContext] = None

    candlestick: Optional[DecisionContext] = None

    relative_strength: Optional[DecisionContext] = None

    trade_plan: Optional[dict] = None

    position_size: Optional[dict] = None