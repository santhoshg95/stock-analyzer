"""The canonical end-to-end daily trading recommendation workflow."""

from __future__ import annotations

from collections import Counter
from datetime import date
from typing import Any

from src.sector.sector_mapper import SectorMapper
from src.news.analysis_service import NewsAnalysisService
from src.workflow.context_enrichment import ContextEnrichment
from src.learning.outcome_repository import OutcomeRepository
from src.workflow.decision_policy import (
    classify_setup, market_alignment, normalize_market_regime,
    option_confidence_status, pcr_adjustment, market_risk_scale,
)


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
    def _option_rejection(option: dict[str, Any]) -> dict[str, Any]:
        """Normalize JSON null and absent rejection payloads to a dictionary."""
        return option.get("rejection") or {}

    @staticmethod
    def _technical_probability(candidate: dict[str, Any], news_score: float = 0) -> float:
        # A transparent heuristic, capped below certainty.  It is deliberately
        # labelled as an estimate until calibrated against recorded outcomes.
        score = candidate["technical_score"]
        confidence = candidate["confidence"]
        breakout = candidate.get("breakout", {}).get("score", 0)
        return round(min(95, max(0, score * 0.60 + confidence * 0.25 + breakout * 3 + news_score * 0.10)), 2)

    @staticmethod
    def _trade_readiness(analysis: dict, candidate: dict, alignment: dict,
                         sector_data: dict, option: dict, setup: str,
                         seasonality: dict | None = None,
                         regime_history: dict | None = None) -> dict:
        """Expose the exact conditions that would promote a watchlist setup."""
        breakout = analysis["breakout"].get("confirmed", False)
        entry_confirmed = analysis.get("setup_evaluation", {}).get("stage_2", {}).get("eligible", False)
        reversal_needed = setup in {"BULLISH_PULLBACK", "BEARISH_BOUNCE"}
        reversal_seen = analysis["candlestick"].get("signal") in {"BUY", "SELL"}
        checks = [
            {"name": "technical_score", "passed": candidate["technical_score"] >= 55,
             "detail": f"{candidate['technical_score']}/100 (minimum 55)"},
            {"name": "entry_confirmation", "passed": entry_confirmed,
             "detail": "all confirmation checks passed" if entry_confirmed else "waiting for EMA20, candle, higher-low, volume and MACD confirmation"},
            {"name": "volume", "passed": analysis["analysis"]["relative_volume"] >= .75,
             "detail": f"relative volume {analysis['analysis']['relative_volume']:.2f}x (minimum 0.75x)"},
            {"name": "market_alignment", "passed": alignment["status"] != "CONFLICT",
             "detail": alignment["status"]},
            {"name": "sector_support", "passed": not sector_data.get("available") or sector_data.get("score", 50) >= 50,
             "detail": sector_data.get("rating", "UNAVAILABLE")},
            {"name": "risk_reward", "passed": candidate["trade_plan"]["risk_reward"] >= 1.5,
             "detail": f"1:{candidate['trade_plan']['risk_reward']} (minimum 1:1.5)"},
            {"name": "option_execution", "passed": option.get("available", False),
             "detail": "executable structure available" if option.get("available") else option.get("reason", "option data unavailable")},
        ]
        seasonality = seasonality or {}
        checks.append({
            "name": "current_month_history",
            "passed": (seasonality.get("sample_quality") in {"ROBUST", "LIMITED"}
                       and seasonality.get("score", 50) >= 45),
            "detail": (f"{seasonality.get('month_name', 'month')} win rate "
                       f"{seasonality.get('win_rate_percent', 'N/A')}% across "
                       f"{seasonality.get('sample_years', 0)} years ({seasonality.get('sample_quality', 'INSUFFICIENT')})"),
        })
        regime_history = regime_history or {}
        checks.append({
            "name": "regime_history",
            "passed": (regime_history.get("sample_quality") in {"ROBUST", "LIMITED"}
                       and (regime_history.get("win_rate_percent") or 0) >= 50),
            "detail": (f"{regime_history.get('regime', 'UNAVAILABLE')} regime: "
                       f"{regime_history.get('win_rate_percent', 'N/A')}% historical win rate across "
                       f"{regime_history.get('sample_count', 0)} samples"),
        })
        passed = sum(item["passed"] for item in checks)
        percentage = round(passed * 100 / len(checks)) if checks else 0
        classification = "READY" if percentage >= 85 else "WATCH" if percentage >= 70 else "WAIT" if percentage >= 50 else "IGNORE"
        return {"ready": classification == "READY", "passed": passed, "total": len(checks),
                "percentage": percentage, "classification": classification,
                "checks": checks, "next_actions": [item["detail"] for item in checks if not item["passed"]]}

    @staticmethod
    def _rank_sectors(reviewed: list[dict], sector_strength: dict) -> list[dict]:
        grouped: dict[str, list[dict]] = {}
        for trade in reviewed:
            if trade["sector"] != "UNKNOWN":
                grouped.setdefault(trade["sector"], []).append(trade)
        rows = []
        for sector, items in grouped.items():
            context = sector_strength.get(sector, {})
            candidate_score = sum(item["ai_score"] for item in items) / len(items)
            index_available = context.get("available", False)
            index_score = context.get("score", 50)
            # Candidate quality remains useful when a Yahoo sector index is unavailable.
            rank_score = candidate_score * .6 + index_score * .4
            rows.append({"sector": sector, "score": round(rank_score, 2),
                         "index_score": index_score, "index_available": index_available,
                         "rating": context.get("rating", "UNAVAILABLE"),
                         "candidate_count": len(items),
                         "average_candidate_score": round(candidate_score, 2)})
        rows.sort(key=lambda item: (item["score"], item["candidate_count"]), reverse=True)
        for rank, row in enumerate(rows, 1):
            row["rank"] = rank
        return rows

    @staticmethod
    def _conflict_gate(candidate: dict[str, Any], option: dict[str, Any], news: dict[str, Any]) -> dict[str, Any]:
        """Reject only critical news, execution, and data-quality failures."""
        conflicts = []
        critical_conflicts = []
        headlines = " ".join(item.get("title", "") for item in news.get("headlines", [])).lower()
        negative_phrases = ("don't buy", "do not buy", "sell", "avoid", "downgrade", "fraud", "probe")
        if news.get("sentiment") == "BEARISH" or any(phrase in headlines for phrase in negative_phrases):
            critical_conflicts.append("negative news or explicit negative analyst headline")
        if news.get("events"):
            critical_conflicts.append("news risk event: " + ", ".join(news["events"]))
        if candidate["action"] in {"BUY", "BUY ON DIP"}:
            if option.get("pcr") is not None and option["pcr"] < .8:
                conflicts.append(f"bearish PCR ({option['pcr']})")
            if option.get("confidence") is not None and option["confidence"] < 50:
                conflicts.append(f"weak option-chain confidence ({option['confidence']}%) — score adjustment only")
            entry_validation = option.get("entry_validation", {})
            if entry_validation and not entry_validation.get("approved", True):
                # Option execution can block the derivative structure, but it
                # must never reject an otherwise valid stock trade.
                conflicts.extend(entry_validation.get("reasons", []))
        conflicts = critical_conflicts + conflicts
        return {"approved": not critical_conflicts, "conflicts": conflicts,
                "critical_conflicts": critical_conflicts,
                "decision": "APPROVED" if not critical_conflicts else "EXCLUDED"}

    def _trade(self, rank: int, candidate: dict[str, Any], market: dict[str, Any], sector_strength: dict[str, Any]) -> dict[str, Any]:
        plan = candidate["trade_plan"]
        analysis = self.platform.analyze(candidate["symbol"])
        sector = self.sectors.get_sector(candidate["symbol"])
        sector_data = sector_strength.get(sector, {"available": False, "score": 50, "rating": "UNAVAILABLE"})
        relative_strength = ContextEnrichment(self.platform.settings.market_data_source == "kite").relative_strength(candidate["symbol"])
        option = candidate.get("options", {"available": False})
        seasonality = candidate.get("current_month_seasonality", {})
        regime_history = candidate.get("regime_history", {})
        direction = "BULLISH" if candidate["action"] in {"BUY", "BUY ON DIP", "WATCH"} else "BEARISH"
        normalized_regime = normalize_market_regime(market.get("regime", "UNAVAILABLE"), market.get("confidence", 0))
        alignment = market_alignment(normalized_regime, market.get("confidence", 0), direction)
        risk_scale = market_risk_scale(market.get("confidence", 0), market.get("available", False))
        base_risk = candidate["position_size"]
        scaled_quantity = int(base_risk.get("quantity", 0) * risk_scale)
        scaled_risk = {**base_risk, "quantity": scaled_quantity,
                       "capital_used": round(base_risk.get("capital_used", 0) * risk_scale, 2),
                       "risk_amount": round(base_risk.get("risk_amount", 0) * risk_scale, 2),
                       "actual_risk": round(base_risk.get("actual_risk", 0) * risk_scale, 2),
                       "market_confidence_scale": risk_scale,
                       "effective_risk_percent": round(self.platform.settings.risk_percent * risk_scale, 3)}
        option_trade = option.get("trade", {})
        scaled_option_risk = round(self.platform.settings.option_risk_per_trade * risk_scale, 2)
        if option.get("available") and option_trade.get("maximum_loss", 0) > scaled_option_risk:
            reason = "Maximum option loss exceeds the market-confidence-adjusted risk budget."
            option = {**option, "available": False, "reason": reason,
                      "rejection": {"code": "SCALED_RISK_BUDGET_EXCEEDED", "category": "RISK",
                                    "reason": reason, "maximum_loss": option_trade["maximum_loss"],
                                    "available_budget": scaled_option_risk}}
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
        option_status = option_confidence_status(option.get("confidence"))
        option_rejection_code = self._option_rejection(option).get("code")
        budget_only_option_failure = option_rejection_code in {
            "RISK_BUDGET_EXCEEDED", "CAPITAL_REQUIRED_EXCEEDED", "SCALED_RISK_BUDGET_EXCEEDED",
        }
        option_score = 50 + pcr_adjustment(option.get("pcr"), direction)
        if option_status == "CONFIRMED":
            option_score += 15
        elif option_status == "CONFLICT":
            option_score -= 10
        elif option_status in {"UNRELIABLE", "UNAVAILABLE"}:
            option_score -= 15
        sector_score = sector_data.get("score", 50)
        relative_score = relative_strength.get("score", 50) if relative_strength.get("available") else 50
        unified_score = round(min(100, max(0,
            candidate["technical_score"] * .55 + alignment["score"] * .15 + sector_score * .10
            + relative_score * .10 + candidate["stock_liquidity"]["score"] * .06 + option_score * .04
            - alignment["penalty"])), 2)
        # Seasonality is contextual: at most +/-1.5 points and only with five
        # or more observations. Regime history carries more weight (up to 3).
        seasonality_adjustment = 0.0
        if seasonality.get("sample_years", 0) >= 5:
            seasonality_adjustment = max(-1.5, min(1.5, (seasonality.get("score", 50) - 50) * .03))
            unified_score = round(min(100, max(0, unified_score + seasonality_adjustment)), 2)
        regime_adjustment = 0.0
        if regime_history.get("sample_count", 0) >= 15 and regime_history.get("win_rate_percent") is not None:
            regime_adjustment = max(-3, min(3, (regime_history["win_rate_percent"] - 50) * .12))
            unified_score = round(min(100, max(0, unified_score + regime_adjustment)), 2)
        setup_evaluation = analysis.get("setup_evaluation", {})
        setup = setup_evaluation.get("stage_1", {}).get("category") or classify_setup(
            analysis["analysis"]["trend"], analysis["analysis"]["rsi_signal"]
        )
        entry_eligible = setup_evaluation.get("stage_2", {}).get("eligible", False)
        probability = self._technical_probability({**candidate, "breakout": analysis["breakout"]}, news["score"])
        calibrated_probability = self.outcomes.contextual_probability(setup, normalized_regime)
        if calibrated_probability is None:
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
        low_risk_reward = plan["risk_reward"] < 1.5
        # Reversal candidates remain observable while their entry develops;
        # inadequate R:R still makes them ineligible for an actual trade.
        risk_reward_rejects_setup = low_risk_reward and setup != "REVERSAL CANDIDATE"
        critical_failure = (not validation["approved"] or risk_reward_rejects_setup
                            or plan["stop_loss"] <= 0 or scaled_quantity <= 0)
        if critical_failure or unified_score < 55:
            status = "REJECTED"
        elif (not entry_eligible or unified_score < 70 or setup in {"BULLISH_PULLBACK", "BEARISH_BOUNCE", "REVERSAL CANDIDATE"}
              or (option_status in {"CONFLICT", "UNRELIABLE", "UNAVAILABLE"} and not budget_only_option_failure)
              or (market.get("confidence", 0) >= 65 and alignment["status"] == "CONFLICT")):
            status = "WATCHLIST"
        else:
            status = "TRADE"
        status_reasons = list(validation["critical_conflicts"])
        if plan["risk_reward"] < 1.5:
            status_reasons.append(f"Risk/reward {plan['risk_reward']}:1 is below the 1.5 minimum.")
        if plan["stop_loss"] <= 0:
            status_reasons.append("Stop-loss is invalid.")
        if scaled_quantity <= 0:
            status_reasons.append("Market-confidence-adjusted position size is below one share.")
        if unified_score < 55:
            status_reasons.append(f"Final score {unified_score} is below 55.")
        if status == "WATCHLIST":
            if unified_score < 70:
                status_reasons.append(f"Final score {unified_score} has not reached the 70 trade threshold.")
            if not entry_eligible:
                missing = setup_evaluation.get("stage_2", {}).get("missing", [])
                status_reasons.append("Entry confirmation missing: " + ", ".join(missing))
            if option_status in {"CONFLICT", "UNRELIABLE", "UNAVAILABLE"} and not budget_only_option_failure:
                rejection = self._option_rejection(option)
                status_reasons.append(rejection.get("reason", f"Option confirmation is {option_status}."))
            if market.get("confidence", 0) >= 65 and alignment["status"] == "CONFLICT":
                status_reasons.append("Trade direction conflicts with a confirmed market regime.")
        eligibility = {"eligible": status == "TRADE", "status": status,
                       "blocking_reasons": status_reasons,
                       "model_confidence_does_not_imply_eligibility": True}
        readiness = self._trade_readiness(analysis, candidate, alignment, sector_data, option, setup,
                                          seasonality, regime_history)
        trade = {
            "rank": rank,
            "symbol": candidate["symbol"],
            "sector": sector,
            "current_price": candidate["current_price"],
            "ai_score": unified_score,
            "technical_score": candidate["technical_score"],
            "confidence": candidate["confidence"],
            "model_confidence": {"decision_confidence": candidate["confidence"],
                                 "estimated_probability": probability,
                                 "calibrated_probability": calibrated_probability},
            "trade_eligibility": eligibility,
            "trade_readiness": readiness,
            "current_month_seasonality": {**seasonality, "score_adjustment": round(seasonality_adjustment, 2)},
            "regime_history": {**regime_history, "score_adjustment": round(regime_adjustment, 2)},
            "risk_policy": {"configured_risk_percent": self.platform.settings.risk_percent,
                            "effective_risk_percent": scaled_risk["effective_risk_percent"],
                            "market_confidence": market.get("confidence", 0), "position_scale": risk_scale},
            "option_budget_policy": {"capital_available": self.platform.settings.option_capital,
                                     "risk_per_trade": self.platform.settings.option_risk_per_trade,
                                     "confidence_adjusted_risk": scaled_option_risk,
                                     "stock_eligibility_independent": True},
            "probability": probability,
            "strategy": "Swing Breakout" if analysis["breakout"]["confirmed"] else candidate["action"],
            "status": status,
            "setup": setup,
            "action": "WAIT FOR CONFIRMATION" if not entry_eligible else candidate["action"],
            "market_alignment": alignment,
            "option_status": option_status,
            "status_reasons": status_reasons,
            "time_frame": "3-5 trading days",
            "technical": {
                "trend": analysis["analysis"]["trend"],
                "trend_stars": self._stars(candidate["technical_score"]),
                "momentum": setup_evaluation.get("momentum_label", analysis["analysis"]["rsi_signal"]),
                "setup_evaluation": setup_evaluation,
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
            "risk": scaled_risk,
            "stock_liquidity": candidate["stock_liquidity"],
            "trust": candidate["trust"],
            "option_strategy": option,
            "news": news,
            "market_context": {**market, "regime": normalized_regime},
            "sector_context": {"sector": sector, **sector_data},
            "relative_strength": relative_strength,
            "ai_reasoning": reasons,
            "recommendation": candidate["action"],
            "calibrated_probability": calibrated_probability,
            "validation": validation,
        }
        if status == "TRADE":
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
        rejected = [trade for trade in reviewed if trade["status"] == "REJECTED"]
        watchlist = [trade for trade in reviewed if trade["status"] == "WATCHLIST"]
        trades = [trade for trade in reviewed if trade["status"] == "TRADE"][:limit]
        for index, trade in enumerate(trades, start=1):
            trade["rank"] = index
        for index, trade in enumerate(watchlist, start=1):
            trade["rank"] = index
        sectors = Counter(trade["sector"] for trade in trades if trade["sector"] != "UNKNOWN")
        bullish = sum(1 for trade in trades if trade["recommendation"] in {"BUY", "BUY ON DIP"})
        market = normalize_market_regime(market_context["regime"], market_context["confidence"]) if market_context["available"] else ("BULLISH" if bullish > len(trades) / 2 else "NEUTRAL")
        average_probability = round(sum(item["probability"] for item in trades) / len(trades), 2) if trades else 0
        average_watchlist_probability = round(sum(item["probability"] for item in watchlist) / len(watchlist), 2) if watchlist else None
        option_strategies = Counter(
            item["option_strategy"].get("strategy") for item in trades
            if item["option_strategy"].get("available") and item["option_strategy"].get("strategy")
        )
        stage_counts = ranked.get("statistics", {})
        historical_learning = self.outcomes.learning_summary()
        sector_ranking = self._rank_sectors(reviewed, sector_strength)
        context_statistics = {
            "news": {
                "passed": sum(1 for item in reviewed if item["news"].get("available") and item["news"].get("sentiment") != "BEARISH" and not item["news"].get("events")),
                "failed": sum(1 for item in reviewed if item["news"].get("available") and (item["news"].get("sentiment") == "BEARISH" or item["news"].get("events"))),
                "unavailable": sum(1 for item in reviewed if not item["news"].get("available")),
            },
            "sector": {
                "passed": sum(1 for item in reviewed if item["sector_context"].get("available") and item["sector_context"].get("score", 50) >= 50),
                "failed": sum(1 for item in reviewed if item["sector_context"].get("available") and item["sector_context"].get("score", 50) < 50),
                "unavailable": sum(1 for item in reviewed if not item["sector_context"].get("available")),
            },
            "relative_strength": {
                "passed": sum(1 for item in reviewed if item["relative_strength"].get("available") and item["relative_strength"].get("score", 50) >= 50),
                "failed": sum(1 for item in reviewed if item["relative_strength"].get("available") and item["relative_strength"].get("score", 50) < 50),
                "unavailable": sum(1 for item in reviewed if not item["relative_strength"].get("available")),
            },
        }
        trust_passed = stage_counts.get("trust_passed", len(ranked["suggestions"]))
        risk_valid = sum(1 for item in reviewed if item["levels"]["risk_reward"] >= 1.5 and item["levels"]["stop_loss"] > 0)
        filter_stages = [
            {"stage": "universe", "input": ranked["universe_size"], "passed": ranked["universe_size"], "rejected": 0},
            {"stage": "analysis", "input": ranked["universe_size"], "passed": stage_counts.get("analysis_succeeded", 0), "rejected": stage_counts.get("analysis_failed", 0)},
            {"stage": "technical", "input": stage_counts.get("analysis_succeeded", 0), "passed": stage_counts.get("technical_passed", 0), "rejected": max(0, stage_counts.get("analysis_succeeded", 0) - stage_counts.get("technical_passed", 0))},
            {"stage": "liquidity", "input": stage_counts.get("technical_passed", 0), "passed": stage_counts.get("liquidity_passed", 0), "rejected": max(0, stage_counts.get("technical_passed", 0) - stage_counts.get("liquidity_passed", 0))},
            {"stage": "trust", "input": stage_counts.get("liquidity_passed", 0), "passed": trust_passed, "rejected": max(0, stage_counts.get("liquidity_passed", 0) - trust_passed)},
            {"stage": "ranking_shortlist", "input": trust_passed, "passed": len(reviewed), "rejected": 0,
             "deferred": max(0, trust_passed - len(reviewed))},
            {"stage": "context_review", "input": len(reviewed), "passed": len(reviewed), "rejected": 0},
            {"stage": "risk", "input": len(reviewed), "passed": risk_valid, "rejected": len(reviewed) - risk_valid},
            {"stage": "final_trade", "input": len(reviewed), "passed": len(trades), "rejected": len(reviewed) - len(trades)},
        ]
        return {
            "report_type": "daily_trading_assistant",
            "date": date.today().isoformat(),
            "market": {**market_context, "regime": market, "confidence": market_context["confidence"] if market_context["available"] else round(sum(item["confidence"] for item in trades) / len(trades), 2) if trades else 0},
            "trades": trades,
            "watchlist": watchlist,
            "sector_ranking": sector_ranking,
            "filter_stages": filter_stages,
            "context_statistics": context_statistics,
            "historical_learning": historical_learning,
            "rejected": [
                {"symbol": trade["symbol"], "technical_score": trade["technical_score"],
                 "reasons": trade["status_reasons"] or trade["validation"]["conflicts"]}
                for trade in rejected
            ],
            "summary": {
                "market": market,
                "best_sector": sector_ranking[0]["sector"] if sector_ranking else "NOT AVAILABLE",
                "best_option_strategy": option_strategies.most_common(1)[0][0] if option_strategies else "NOT AVAILABLE",
                "stocks_scanned": ranked["universe_size"],
                "stocks_qualified": len(ranked["suggestions"]),
                "analysis_succeeded": stage_counts.get("analysis_succeeded", len(ranked["suggestions"])),
                "analysis_failed": stage_counts.get("analysis_failed", max(0, ranked["universe_size"] - len(ranked["suggestions"]))),
                "technical_passed": stage_counts.get("technical_passed", len(ranked["suggestions"])),
                "liquidity_passed": stage_counts.get("liquidity_passed", len(ranked["suggestions"])),
                "trust_passed": trust_passed,
                "context_reviewed": len(reviewed),
                "risk_valid": risk_valid,
                "market_aligned": sum(1 for item in reviewed if item["market_alignment"]["status"] == "ALIGNED"),
                "watchlisted": len(watchlist),
                "option_confirmed": sum(1 for item in reviewed if item["option_status"] == "CONFIRMED"),
                "rejected": len(rejected),
                "conflicts_rejected": sum(1 for item in rejected if item["validation"]["critical_conflicts"]),
                "stocks_shortlisted": len(trades) + len(watchlist),
                "trades_generated": len(trades),
                "average_probability": average_probability if trades else None,
                "average_watchlist_probability": average_watchlist_probability,
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
