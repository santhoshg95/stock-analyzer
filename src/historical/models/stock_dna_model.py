from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class StockDNAModel:
    """
    Permanent behavioural profile of a stock.
    """

    symbol: str

    trend_type: str = "UNKNOWN"

    volatility_type: str = "UNKNOWN"

    liquidity_type: str = "UNKNOWN"

    momentum_type: str = "UNKNOWN"

    gap_type: str = "UNKNOWN"

    volume_type: str = "UNKNOWN"

    option_liquidity: str = "UNKNOWN"

    premium_quality: str = "UNKNOWN"

    seasonality_type: str = "UNKNOWN"

    market_personality: str = "UNKNOWN"

    preferred_strategy: str = "UNKNOWN"

    strengths: List[str] = field(default_factory=list)

    weaknesses: List[str] = field(default_factory=list)

    notes: Dict = field(default_factory=dict)