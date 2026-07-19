"""
Stock Context

Central object shared across the entire AI pipeline.
"""

from dataclasses import dataclass, field
from typing import Any

from src.decision.models.decision import Decision
from src.evidence.models.evidence_collection import EvidenceCollection
from src.factors.models.factor_analysis import FactorAnalysis
from src.options.models.option_context import OptionContext
from src.strategy.models.trading_strategy import TradingStrategy
from src.trade.models.trade_plan import TradePlan


@dataclass(slots=True)
class StockContext:
    """
    Shared context object used throughout the AI trading platform.
    """

    symbol: str

    # Existing Analysis
    analysis: Any = None

    # Market Intelligence
    market: Any = None

    sector: Any = None

    technical: Any = None

    # News Intelligence
    news: Any = None

    # Options Intelligence
    options: OptionContext | None = None

    # Explainable AI
    evidence: EvidenceCollection | None = None

    # Factor Engine
    factors: FactorAnalysis | None = None

    # Decision Engine
    decision: Decision | None = None

    # Strategy Engine
    strategy: TradingStrategy | None = None

    # Trade Planner
    trade: TradePlan | None = None

    metadata: dict = field(default_factory=dict)