"""
Master Trade Report

This is the primary model used throughout
the AI Trading Platform.

Every engine contributes to this object.
"""

from dataclasses import dataclass
from typing import Optional

from src.models.stock_analysis import StockAnalysis
from src.models.trade_plan import TradePlan
from src.models.position_size import PositionSize
from src.models.decision import Decision


@dataclass
class TradeReport:

    analysis: StockAnalysis

    entry: dict

    breakout: dict

    trade_plan: Optional[TradePlan] = None

    position_size: Optional[PositionSize] = None

    decision: Optional[Decision] = None

    ai_summary: Optional[str] = None