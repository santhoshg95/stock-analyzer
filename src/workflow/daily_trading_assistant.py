"""The canonical end-to-end daily trading recommendation workflow."""

from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Any

from src.sector.sector_mapper import SectorMapper
from src.news.analysis_service import NewsAnalysisService
from src.workflow.context_enrichment import ContextEnrichment
from src.learning.outcome_repository import OutcomeRepository


class DailyTradingAssistant:
    """Transform ranked analyses into the architecture's final daily output.

    The workflow consumes the public platform facade so data-source, paper
    trading, validation, and error behaviour remain consistent everywhere.
    """

    def __init__(self, platform):
        self.platform = platform
        self.sectors = SectorMapper()
        self.outcomes = OutcomeRepository()

    @staticmethod
    def _stars(score: float, maximum: float = 100) -> str:
        filled = max(0, min(5, round((score / maximum) * 5)))
        return "★" * filled + "☆" * (5 - filled)

    @staticmethod
    def _technical_probability(candidate: dict[str, Any], news_score: float = 0) -> float:
        # A transparent heuristic, capped below certainty.  It is deliberately
        # labelled as an estimate until calibrated against recorded outcomes.
        score = candidate["technical_score"]
        confidence = candidate["confidence"]
        breakout = candidate.get("breakout", {}).get("score", 0)
        return round(min(95, max(0, score * 0.60 + confidence * 0.25 + breakout * 3 + news_score * 0.10)), 2)

    @staticmethod
    def _conflict_gate(candidate: dict[str, Any], option: dict[str, Any], news: dict[str, Any]) -> dict[str, Any]:
        """Block technical longs when independent evidence materially disagrees."""
        conflicts = []
        headlines = " ".join(item.get("title", "") for item in news.get("headlines", [])).lower()
        negative_phrases = ("don't buy", "do not buy", "sell", "avoid", "downgrade", "fraud", "probe")
        if news.get("sentiment") == "BEARISH" or any(phrase in headlines for phrase in negative_phrases):
            conflicts.append("negative news or explicit negative analyst headline")
        if news.get("events"):
            conflicts.append("news risk event: " + ", ".join(news["events"]))
        # Preserve PCR/confidence evidence even when an option trade cannot be
        # sized. Lot affordability affects only the option recommendation, not
        # whether an otherwise valid stock setup reaches the shortlist.
        if candidate["action"] in {"BUY", "BUY ON DIP"} and (option.get("pcr") is not None or option.get("confidence") is not None):
            if option.get("pcr") is not None and option["pcr"] < 0.8:
                conflicts.append(f"bearish PCR ({option['pcr']})")
            if option.get("confidence", 0) < 45:
                conflicts.append(f"weak option-chain confidence ({option.get('confidence')}%)")
        return {"approved": not conflicts, "conflicts": conflicts,
                "decision": "APPROVED" if not conflicts else "EXCLUDED"}

    def _trade(self, rank: int, candidate: dict[str, Any], market: dict[str, Any], sector_strength: dict[str, Any]) -> dict[str, Any]:
        plan = candidate["trade_plan"]
        analysis = self.platform.analyze(candidate["symbol"])
        sector = self.sectors.get_sector(candidate["symbol"])
        sector_data = sector_strength.get(sector, {"score": 0, "rating": "UNAVAILABLE"})
        relative_strength = ContextEnrichment(self.platform.settings.market_data_source == "kite").relative_strength(candidate["symbol"])
        option = candidate.get("options", {"available": False})
        # Offline/cache mode must remain deterministic and must not make hidden
        # network calls. Live reports fetch news only for these finalists.
        if self.platform.settings.market_data_source == "kite":
            news = NewsAnalysisService.analyze(candidate["symbol"])
        else:
            news = {
                "available": False, "score": 0, "sentiment": "UNAVAILABLE",
                "confidence": 0, "article_count": 0, "events": [], "headlines": [],
                "reasons": ["News analysis requires live mode (MARKET_DATA_SOURCE=kite)."],
            }
        validation = self._conflict_gate(candidate, option, news)
        adjustments = news["score"] * 0.15
        if sector_data["score"]:
            adjustments += (sector_data["score"] - 50) * 0.10
        if relative_strength["available"]:
            adjustments += (relative_strength["score"] - 50) * 0.10
        if market["available"]:
            adjustments += market["score"] * 0.05
        unified_score = round(min(100, max(0, candidate["technical_score"] + adjustments)), 2)
        probability = self._technical_probability({**candidate, "breakout": analysis["breakout"]}, news["score"])
        calibrated_probability = self.outcomes.calibrated_probability(candidate["action"])
        if calibrated_probability is not None:
            probability = round((probability * 0.4) + (calibrated_probability * 0.6), 2)
        reasons = [
            candidate["reason"],
            f"Trend: {analysis['analysis']['trend']}.",
            f"RSI: {analysis['analysis']['rsi']:.1f}.",
            f"Relative volume: {analysis['analysis']['relative_volume']:.2f}x.",
            f"Breakout: {'confirmed' if analysis['breakout']['confirmed'] else 'not confirmed'}.",
            f"Candlestick: {analysis['candlestick']['pattern']}.",
        ]
        reasons.extend(option.get("reasons", []))
        reasons.extend(news["reasons"])
        trade = {
            "rank": rank,
            "symbol": candidate["symbol"],
            "sector": sector,
            "current_price": candidate["current_price"],
            "ai_score": unified_score,
            "technical_score": candidate["technical_score"],
            "confidence": candidate["confidence"],
            "probability": probability,
            "strategy": "Swing Breakout" if analysis["breakout"]["confirmed"] else candidate["action"],
            "time_frame": "3-5 trading days",
            "technical": {
                "trend": analysis["analysis"]["trend"],
                "trend_stars": self._stars(candidate["technical_score"]),
                "momentum": analysis["analysis"]["rsi_signal"],
                "volume": analysis["analysis"]["volume_signal"],
                "relative_strength": "NOT AVAILABLE",
                "breakout": analysis["breakout"],
                "candlestick": analysis["candlestick"],
            },
            "levels": {
                "support": analysis["entry"]["support"],
                "resistance": analysis["entry"]["resistance"],
                "entry": plan["entry"],
                "stop_loss": plan["stop_loss"],
                "target_1": plan["target1"],
                "target_2": plan["target2"],
                "target_3": plan["target3"],
                "risk_reward": plan["risk_reward"],
            },
            "risk": candidate["position_size"],
            "stock_liquidity": candidate["stock_liquidity"],
            "trust": candidate["trust"],
            "option_strategy": option,
            "news": news,
            "market_context": market,
            "sector_context": {"sector": sector, **sector_data},
            "relative_strength": relative_strength,
            "ai_reasoning": reasons,
            "recommendation": candidate["action"],
            "calibrated_probability": calibrated_probability,
            "validation": validation,
        }
        if validation["approved"]:
            trade["recommendation_id"] = self.outcomes.record_recommendation(trade)
        else:
            trade["recommendation_id"] = None
        return trade

    def generate(self, limit: int = 15, minimum_score: int = 40) -> dict[str, Any]:
        # Fetch extra technical candidates so rejected news/option conflicts can
        # be replaced instead of leaving a misleading top-15 list.
        ranked = self.platform.suggest_stocks(limit=min(50, max(15, limit * 3)), minimum_score=minimum_score)
        enrichment = ContextEnrichment(self.platform.settings.market_data_source == "kite")
        market_context, sector_strength = enrichment.market_and_sectors()
        reviewed = [self._trade(index, candidate, market_context, sector_strength) for index, candidate in enumerate(ranked["suggestions"], start=1)]
        rejected = [trade for trade in reviewed if not trade["validation"]["approved"]]
        trades = [trade for trade in reviewed if trade["validation"]["approved"]][:limit]
        for index, trade in enumerate(trades, start=1):
            trade["rank"] = index
        sectors = Counter(trade["sector"] for trade in trades if trade["sector"] != "UNKNOWN")
        bullish = sum(1 for trade in trades if trade["recommendation"] in {"BUY", "BUY ON DIP"})
        market = market_context["regime"] if market_context["available"] else ("BULLISH" if bullish > len(trades) / 2 else "NEUTRAL")
        average_probability = round(sum(item["probability"] for item in trades) / len(trades), 2) if trades else 0
        option_strategies = Counter(
            item["option_strategy"].get("strategy") for item in trades
            if item["option_strategy"].get("available") and item["option_strategy"].get("strategy")
        )
        return {
            "report_type": "daily_trading_assistant",
            "date": date.today().isoformat(),
            "market": {**market_context, "regime": market, "confidence": market_context["confidence"] if market_context["available"] else round(sum(item["confidence"] for item in trades) / len(trades), 2) if trades else 0},
            "trades": trades,
            "rejected": [
                {"symbol": trade["symbol"], "technical_score": trade["technical_score"],
                 "reasons": trade["validation"]["conflicts"]}
                for trade in rejected
            ],
            "summary": {
                "market": market,
                "best_sector": sectors.most_common(1)[0][0] if sectors else "NOT AVAILABLE",
                "best_option_strategy": option_strategies.most_common(1)[0][0] if option_strategies else "NOT AVAILABLE",
                "stocks_scanned": ranked["universe_size"],
                "stocks_qualified": len(ranked["suggestions"]),
                "conflicts_rejected": len(rejected),
                "stocks_shortlisted": len(trades),
                "trades_generated": len(trades),
                "average_probability": average_probability,
                "highest_ai_score": trades[0]["symbol"] if trades else None,
                "market_risk": "LOW" if market == "BULLISH" else "MODERATE",
                "recommendation": "Take only bullish, risk-defined trades." if market == "BULLISH" else "Wait for clearer market alignment.",
            },
            "limitations": [
                "Probability is a transparent heuristic, not a guaranteed or calibrated win rate.",
                "Relative strength, sector, and news are shown only when a live data integration is available.",
                "Recommendations are for research and paper trading; no live order is submitted.",
            ],
        }
