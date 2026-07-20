"""Live market, sector, and relative-strength enrichment with safe fallbacks."""

from __future__ import annotations

from copy import deepcopy
from threading import Lock
from time import monotonic

from src.market.market_regime import MarketRegime
from src.market.relative_strength import RelativeStrength
from src.market_data.market_data_hub import MarketDataHub
from src.sector.sector_strength import SectorStrength


class ContextEnrichment:
    """Collect context once per report and never fail the core trade scan."""

    _cache_lock = Lock()
    _market_cache = None
    _relative_strength_cache = {}
    market_cache_ttl_seconds = 5 * 60
    relative_strength_cache_ttl_seconds = 15 * 60

    def __init__(self, live: bool):
        self.live = live

    def market_and_sectors(self):
        if not self.live:
            return ({"available": False, "regime": "UNAVAILABLE", "score": 0, "confidence": 0, "indices": {}}, {})
        with self._cache_lock:
            cached = self._market_cache
            if cached and monotonic() - cached[0] < self.market_cache_ttl_seconds:
                return deepcopy(cached[1])
        try:
            snapshot = MarketDataHub().get_market_snapshot()
            regime = MarketRegime.classify(snapshot)
            indices = snapshot.get("india", {})
            result = ({"available": True, "regime": regime.status, "score": regime.score,
                     "confidence": regime.confidence, "reasons": regime.reasons, "indices": indices,
                     "vix": snapshot.get("volatility")}, SectorStrength().analyze())
        except Exception as exc:  # Provider failure must not stop recommendations.
            result = ({"available": False, "regime": "UNAVAILABLE", "score": 0, "confidence": 0,
                     "indices": {}, "reason": exc.__class__.__name__}, {})
        with self._cache_lock:
            type(self)._market_cache = (monotonic(), deepcopy(result))
        return result

    def relative_strength(self, symbol: str):
        if not self.live:
            return {"available": False, "rating": "UNAVAILABLE", "score": 0}
        key = symbol.strip().upper().removesuffix(".NS")
        with self._cache_lock:
            cached = self._relative_strength_cache.get(key)
            if cached and monotonic() - cached[0] < self.relative_strength_cache_ttl_seconds:
                return deepcopy(cached[1])
        try:
            result = RelativeStrength.analyze(symbol)
            if not result:
                value = {"available": False, "rating": "UNAVAILABLE", "score": 0}
            else:
                points = {"VERY STRONG": 100, "STRONG": 80, "OUTPERFORM": 65,
                          "INLINE": 50, "UNDERPERFORM": 20}
                value = {"available": True, **result, "score": points[result["rating"]]}
        except Exception as exc:
            value = {"available": False, "rating": "UNAVAILABLE", "score": 0, "reason": exc.__class__.__name__}
        with self._cache_lock:
            type(self)._relative_strength_cache[key] = (monotonic(), deepcopy(value))
        return value
