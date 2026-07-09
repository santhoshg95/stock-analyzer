"""
Stock Context

Central object shared across the entire AI pipeline.
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class StockContext:

    symbol: str

    # Existing analysis pipeline output
    analysis: Any = None

    # Market Intelligence
    market: Any = None
    sector: Any = None
    technical: Any = None

    # News Intelligence
    news: Any = None

    # Options Intelligence
    option_chain: Any = None

    # AI
    ai_score: Any = None

    # Final Strategy
    strategy: Any = None

    # Trade
    trade: Any = None

    metadata: dict = field(default_factory=dict)