"""
Stock Context

Central object shared across the entire AI pipeline.

Version 2
---------
Extended to support:
- Historical Intelligence
- Stock DNA
- Monthly Watchlist
- Opportunity Ranking
- Qualification
- Confidence
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

    # -----------------------------
    # Basic
    # -----------------------------

    symbol: str

    metadata: dict = field(default_factory=dict)

    # -----------------------------
    # Existing Analysis
    # -----------------------------

    analysis: Any = None

    market: Any = None

    sector: Any = None

    technical: Any = None

    news: Any = None

    options: OptionContext | None = None

    # -----------------------------
    # Historical Intelligence
    # -----------------------------

    historical_profile: Any = None

    stock_dna: Any = None

    monthly_score: float = 0.0

    historical_score: float = 0.0

    seasonality_score: float = 0.0

    # -----------------------------
    # Qualification
    # -----------------------------

    qualified: bool = True

    qualification_reason: str = ""

    # -----------------------------
    # Explainable AI
    # -----------------------------

    evidence: EvidenceCollection | None = None

    factors: FactorAnalysis | None = None

    decision: Decision | None = None

    strategy: TradingStrategy | None = None

    trade: TradePlan | None = None

    # -----------------------------
    # Opportunity Ranking
    # -----------------------------

    technical_score: float = 0.0

    option_score: float = 0.0

    news_score: float = 0.0

    market_score: float = 0.0

    risk_score: float = 0.0

    strategy_score: float = 0.0

    opportunity_score: float = 0.0

    confidence: float = 0.0

    rank: int = 0

    recommendation: str = ""

    # -----------------------------
    # Helper
    # -----------------------------

    @property
    def total_score(self) -> float:

        return (
            self.historical_score
            + self.technical_score
            + self.option_score
            + self.market_score
            + self.news_score
            + self.strategy_score
            - self.risk_score
        )