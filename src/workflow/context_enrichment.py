"""Live market, sector, and relative-strength enrichment with safe fallbacks."""

from __future__ import annotations

from src.market.market_regime import MarketRegime
from src.market.relative_strength import RelativeStrength
from src.market_data.market_data_hub import MarketDataHub
from src.sector.sector_strength import SectorStrength


class ContextEnrichment:
    """Collect context once per report and never fail the core trade scan."""

    def __init__(self, live: bool):
        self.live = live

    def market_and_sectors(self):
        if not self.live:
            return ({"available": False, "regime": "UNAVAILABLE", "score": 0, "confidence": 0, "indices": {}}, {})
        try:
            snapshot = MarketDataHub().get_market_snapshot()
            regime = MarketRegime.classify(snapshot)
            indices = snapshot.get("india", {})
            return ({"available": True, "regime": regime.status, "score": regime.score,
                     "confidence": regime.confidence, "reasons": regime.reasons, "indices": indices,
                     "vix": snapshot.get("volatility")}, SectorStrength().analyze())
        except Exception as exc:  # Provider failure must not stop recommendations.
            return ({"available": False, "regime": "UNAVAILABLE", "score": 0, "confidence": 0,
                     "indices": {}, "reason": exc.__class__.__name__}, {})

    def relative_strength(self, symbol: str):
        if not self.live:
            return {"available": False, "rating": "UNAVAILABLE", "score": 0}
        try:
            result = RelativeStrength.analyze(symbol)
            if not result:
                return {"available": False, "rating": "UNAVAILABLE", "score": 0}
            points = {"VERY STRONG": 100, "STRONG": 80, "OUTPERFORM": 65,
                      "INLINE": 50, "UNDERPERFORM": 20}
            return {"available": True, **result, "score": points[result["rating"]]}
        except Exception as exc:
            return {"available": False, "rating": "UNAVAILABLE", "score": 0, "reason": exc.__class__.__name__}
