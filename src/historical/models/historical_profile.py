from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class HistoricalProfile:
    """
    Stores all historical intelligence about a stock.
    This object is shared across the complete analysis pipeline.
    """

    symbol: str

    history_years: float = 0.0

    # Returns
    cagr: float = 0.0
    annual_return: float = 0.0
    monthly_return: float = 0.0
    weekly_return: float = 0.0
    daily_return: float = 0.0

    # Risk
    volatility: float = 0.0
    downside_volatility: float = 0.0
    max_drawdown: float = 0.0
    beta: float = 0.0

    # Ratios
    sharpe_ratio: float = 0.0
    sortino_ratio: float = 0.0
    calmar_ratio: float = 0.0

    # Behaviour
    win_rate: float = 0.0
    loss_rate: float = 0.0

    avg_gain: float = 0.0
    avg_loss: float = 0.0

    avg_gap_up: float = 0.0
    avg_gap_down: float = 0.0

    avg_volume: float = 0.0

    # Monthly statistics
    monthly_returns: Dict[str, float] = field(default_factory=dict)

    monthly_win_rate: Dict[str, float] = field(default_factory=dict)

    seasonality_score: float = 0.0

    # Liquidity
    liquidity_score: float = 0.0

    # Premium Behaviour
    premium_quality_score: float = 0.0

    # Consistency
    consistency_score: float = 0.0

    # Overall
    historical_score: float = 0.0

    # Recommendation
    preferred_strategy: Optional[str] = None

    # Attached DNA object
    stock_dna: Optional["StockDNAModel"] = None

    metadata: Dict = field(default_factory=dict)
