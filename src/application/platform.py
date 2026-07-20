"""The supported, safe entry point for analysis, backtesting, and paper trading."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import re
from time import sleep
from threading import Lock
from typing import Any

import numpy as np
import pandas as pd
from kiteconnect.exceptions import TokenException
from requests.exceptions import RequestException

from src.application.errors import (
    AuthenticationError,
    DataUnavailableError,
    OrderError,
    ValidationError,
)
from src.application.settings import PlatformSettings
from src.backtesting.backtester import Backtester
from src.backtesting.metrics import Metrics
from src.broker.paper_broker import PaperBroker
from src.data_provider.provider import DataProvider
from src.data_provider.kite_data_provider import KiteDataProvider
from src.indicators.pipeline import IndicatorPipeline
from src.position_sizing.position_size import PositionSizingEngine
from src.options.engine.option_engine import OptionEngine
from src.options.kite_option_chain import KiteOptionChainProvider
from src.options.trade_builder import OptionTradeBuilder
from src.options.entry_validator import OptionEntryValidator
from src.trade_plan.trade_plan import TradePlanEngine
from src.trading_engine.engine import TradingEngine
from src.workflow.daily_trading_assistant import DailyTradingAssistant
from src.learning.outcome_repository import OutcomeRepository
from src.historical.current_month_seasonality import CurrentMonthSeasonality
from src.historical.regime_performance import RegimePerformance


class TradingPlatform:
    """Facade that keeps callers independent from individual analysis engines.

    Live trading is intentionally unavailable here.  Use ``paper_trade`` to
    simulate orders against the latest analysis price.
    """

    def __init__(self, settings: PlatformSettings | None = None, paper_broker: PaperBroker | None = None):
        self.settings = settings or PlatformSettings.from_environment()
        self.provider = (
            KiteDataProvider()
            if self.settings.market_data_source == "kite"
            else DataProvider()
        )
        self.engine = TradingEngine(provider=self.provider)
        self.paper_broker = paper_broker or PaperBroker(starting_cash=self.settings.capital)
        self._option_chain_provider = None

    @staticmethod
    def _symbol(symbol: str) -> str:
        clean = symbol.strip().upper() if isinstance(symbol, str) else ""
        if not clean or len(clean) > 30 or not re.fullmatch(r"[A-Z0-9.&-]+", clean):
            raise ValidationError(
                "symbol must contain letters, numbers, dots, ampersands, or hyphens"
            )
        return clean.removesuffix(".NS")

    @staticmethod
    def _serialize(value: Any) -> Any:
        if is_dataclass(value):
            return {key: TradingPlatform._serialize(item) for key, item in asdict(value).items()}
        if isinstance(value, dict):
            return {str(key): TradingPlatform._serialize(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [TradingPlatform._serialize(item) for item in value]
        if isinstance(value, (np.integer, np.floating)):
            return value.item()
        if isinstance(value, pd.Timestamp):
            return value.isoformat()
        return value

    @staticmethod
    def _stock_liquidity(analysis: dict[str, Any]) -> dict[str, Any]:
        """Score cash-market liquidity using average daily traded value.

        Relative volume describes today's participation; average traded value
        determines whether a stock is normally practical to enter and exit.
        """
        average_turnover = analysis["current_price"] * analysis["average_volume"]
        turnover_crore = average_turnover / 10_000_000
        if turnover_crore >= 100:
            base, status = 100, "EXCELLENT"
        elif turnover_crore >= 50:
            base, status = 85, "HIGH"
        elif turnover_crore >= 20:
            base, status = 70, "GOOD"
        elif turnover_crore >= 5:
            base, status = 50, "MODERATE"
        else:
            base, status = 25, "LOW"
        rvol = analysis["relative_volume"]
        participation = 10 if rvol >= 1 else 0 if rvol >= .75 else -10
        return {
            "score": max(0, min(100, base + participation)),
            "status": status,
            "average_daily_turnover_crore": round(turnover_crore, 2),
            "relative_volume": round(rvol, 2),
        }

    @staticmethod
    def _trust_score(analysis: dict[str, Any], liquidity: dict[str, Any], quality: dict[str, Any]) -> dict[str, Any]:
        """Conservative F&O suitability score; it is not a manipulation claim."""
        atr_percent = (analysis["atr"] / analysis["current_price"]) * 100
        score = liquidity["score"] * .50
        score += 20 if quality["history_days"] >= 200 else 5
        score += 15 if atr_percent <= 5 else 5 if atr_percent <= 8 else 0
        score += 10 if quality["large_return_days"] <= 2 and quality["large_gap_days"] <= 2 else 0
        score = round(min(100, score), 2)
        flags = []
        if quality["large_return_days"] > 2:
            flags.append("frequent extreme daily moves")
        if quality["large_gap_days"] > 2:
            flags.append("frequent large gaps")
        if atr_percent > 8:
            flags.append("very high ATR volatility")
        return {"score": score, "status": "TRUSTED" if score >= 70 else "CAUTION" if score >= 55 else "EXCLUDE",
                "atr_percent": round(atr_percent, 2), "flags": flags}

    def analyze(self, symbol: str) -> dict[str, Any]:
        symbol = self._symbol(symbol)
        try:
            report = self.engine.analyze(symbol)
        except TokenException as exc:
            raise AuthenticationError(
                "Zerodha Kite authentication failed. Update KITE_API_KEY and "
                "generate a fresh KITE_ACCESS_TOKEN before running the platform."
            ) from exc
        except RequestException as exc:
            raise DataUnavailableError(
                "Unable to reach Zerodha Kite. Check your network connection and try again."
            ) from exc
        if report is None:
            raise DataUnavailableError(f"No historical data is available for {symbol}")

        trade_plan = TradePlanEngine.generate(report["entry"])
        position_size = PositionSizingEngine.calculate(
            self.settings.capital,
            self.settings.risk_percent,
            trade_plan.entry,
            trade_plan.stop_loss,
        )
        return self._serialize({
            "symbol": symbol,
            "analysis": report["analysis"],
            "entry": report["entry"],
            "breakout": report["breakout"],
            "candlestick": report["candlestick"],
            "setup_evaluation": report["setup_evaluation"],
            "market_quality": report["market_quality"],
            "decision": report["decision"],
            "trade_plan": trade_plan,
            "position_size": position_size,
        })

    def backtest(self, symbol: str) -> dict[str, Any]:
        symbol = self._symbol(symbol)
        try:
            dataframe = self.provider.get_data(symbol)
        except TokenException as exc:
            raise AuthenticationError(
                "Zerodha Kite authentication failed. Generate a fresh daily "
                "KITE_ACCESS_TOKEN and try again."
            ) from exc
        except RequestException as exc:
            raise DataUnavailableError(
                "Unable to reach Zerodha Kite. Check your network connection and try again."
            ) from exc
        if dataframe is None or dataframe.empty:
            raise DataUnavailableError(f"No historical data is available for {symbol}")
        trades = Backtester.run(IndicatorPipeline.run(dataframe.copy()))
        return {"symbol": symbol, "metrics": Metrics.summarize(trades), "trades": self._serialize(trades)}

    def _universe_symbols(self) -> list[str]:
        """Use Kite's current F&O universe, or cached files in explicit offline mode."""
        if self.settings.market_data_source == "kite":
            try:
                return self.provider.get_symbols()
            except TokenException as exc:
                raise AuthenticationError(
                    "Zerodha Kite authentication failed. Update KITE_API_KEY and "
                    "generate a fresh KITE_ACCESS_TOKEN before running the platform."
                ) from exc
            except RequestException as exc:
                raise DataUnavailableError(
                    "Unable to reach Zerodha Kite. Check your network connection and try again."
                ) from exc
        from src.config.settings import DATA_FOLDER

        if not Path(DATA_FOLDER).exists():
            return []
        return sorted(path.name.removesuffix(".NS.csv") for path in Path(DATA_FOLDER).glob("*.NS.csv"))

    def suggest_stocks(self, limit: int = 5, minimum_score: int = 40) -> dict[str, Any]:
        """Rank the configured stock universe and return actionable setups.

        A candidate must meet the score threshold and receive BUY, BUY ON DIP,
        or WATCH from the decision engine.  Failed analyses are omitted rather
        than allowing a missing data file to stop the entire scan.
        """
        if not isinstance(limit, int) or not 1 <= limit <= 50:
            raise ValidationError("limit must be an integer between 1 and 50")
        if not isinstance(minimum_score, int) or not 0 <= minimum_score <= 100:
            raise ValidationError("minimum_score must be an integer between 0 and 100")

        symbols = self._universe_symbols()
        if not symbols:
            raise DataUnavailableError("No stocks are available to screen")

        stage_counts = {"analysis_succeeded": 0, "analysis_failed": 0,
                        "technical_passed": 0, "liquidity_passed": 0,
                        "trust_passed": 0}
        count_lock = Lock()

        def increment(key: str) -> None:
            with count_lock:
                stage_counts[key] += 1

        def evaluate(symbol: str) -> dict[str, Any] | None:
            try:
                report = self.analyze(symbol)
            except (DataUnavailableError, ValueError, KeyError, TypeError):
                increment("analysis_failed")
                return None
            increment("analysis_succeeded")
            analysis = report["analysis"]
            decision = report["decision"]
            if analysis["score"] < minimum_score or decision["action"] not in {"BUY", "BUY ON DIP", "WATCH"}:
                return None
            increment("technical_passed")
            liquidity = self._stock_liquidity(analysis)
            # Avoid names that are hard to enter/exit even if their chart score
            # is attractive. The threshold is deliberately modest for F&O names.
            if liquidity["score"] < 40:
                return None
            increment("liquidity_passed")
            trust = self._trust_score(analysis, liquidity, report["market_quality"])
            if trust["score"] < 55:
                return None
            increment("trust_passed")
            return {
                "symbol": symbol,
                "action": decision["action"],
                "confidence": decision["confidence"],
                "technical_score": analysis["score"],
                "recommendation": analysis["recommendation"],
                "current_price": analysis["current_price"],
                "stock_liquidity": liquidity,
                "trust": trust,
                "risk_reward": report["trade_plan"]["risk_reward"],
                "candlestick": report["candlestick"],
                "setup_evaluation": report["setup_evaluation"],
                "reason": decision["reason"],
                "trade_plan": report["trade_plan"],
                "position_size": report["position_size"],
            }

        candidates = []
        workers = 1 if self.settings.market_data_source == "kite" else min(8, len(symbols))
        def rate_limited_evaluate(symbol: str) -> dict[str, Any] | None:
            candidate = evaluate(symbol)
            if self.settings.market_data_source == "kite":
                # Kite historical-data calls are rate-limited; retain a margin.
                sleep(0.35)
            return candidate

        with ThreadPoolExecutor(max_workers=workers) as executor:
            futures = [executor.submit(rate_limited_evaluate, symbol) for symbol in symbols]
            for future in as_completed(futures):
                candidate = future.result()
                if candidate:
                    candidates.append(candidate)

        action_rank = {"BUY": 2, "BUY ON DIP": 1, "WATCH": 0}
        candidates.sort(
            key=lambda item: (
                action_rank[item["action"]],
                item["technical_score"],
                item["stock_liquidity"]["score"],
                item["risk_reward"],
            ),
            reverse=True,
        )
        top_candidates = candidates[:limit]
        for candidate in top_candidates:
            historical = self._historical_context(candidate["symbol"])
            candidate["current_month_seasonality"] = historical["current_month"]
            candidate["regime_history"] = historical["regime"]
            candidate["options"] = self._option_trade_plan(candidate)
            option_confidence = candidate["options"].get("confidence", 0)
            candidate["probability"] = round(
                min(95, candidate["technical_score"] * 0.6 + candidate["confidence"] * 0.25 + option_confidence * 0.15),
                2,
            )
            candidate["ai_reasoning"] = [
                candidate["reason"],
                f"Technical score: {candidate['technical_score']}/100.",
                f"Risk/reward: {candidate['risk_reward']}:1.",
                f"Candlestick: {candidate['candlestick']['pattern']} ({candidate['candlestick']['signal']}).",
                *candidate["options"].get("reasons", []),
            ]
        return {
            "universe_size": len(symbols),
            "market_data_source": self.settings.market_data_source,
            "minimum_score": minimum_score,
            "suggestions": top_candidates,
            "statistics": stage_counts,
            "message": (
                "No stocks currently meet the selected criteria."
                if not candidates
                else f"Ranked candidates using {self.settings.market_data_source} daily data."
            ),
        }

    def _option_trade_plan(self, candidate: dict[str, Any]) -> dict[str, Any]:
        """Enrich only final candidates with live option-chain intelligence."""
        if self.settings.market_data_source != "kite":
            return {"available": False, "error_type": "DATA_SOURCE",
                    "rejection": {"code": "LIVE_DATA_REQUIRED", "category": "DATA",
                                  "reason": "Option analysis requires MARKET_DATA_SOURCE=kite."},
                    "reason": "Option analysis requires MARKET_DATA_SOURCE=kite."}
        try:
            if self._option_chain_provider is None:
                self._option_chain_provider = KiteOptionChainProvider(self.provider.provider.kite)
            chain = self._option_chain_provider.get_chain(
                candidate["symbol"], candidate["current_price"]
            )
            analysis = OptionEngine().analyze(chain)
            direction = "BULLISH" if candidate["action"] in {"BUY", "BUY ON DIP"} else "BEARISH"
            trade = OptionTradeBuilder.build(
                chain,
                analysis.suggested_strategy or "Wait",
                direction,
                support=candidate["trade_plan"]["stop_loss"],
                resistance=candidate["trade_plan"]["target1"],
                risk_budget=self.settings.option_risk_per_trade,
                capital_available=self.settings.option_capital,
            )
            validation = OptionEntryValidator.validate(chain, trade, direction)
            rejection = trade.get("rejection")
            if trade["available"] and not validation["approved"]:
                rejection = {"code": "ENTRY_VALIDATION_FAILED", "category": "EXECUTION",
                             "reason": "; ".join(validation["reasons"])}
            return self._serialize({
                "available": trade["available"],
                "reason": trade.get("reason"),
                "expiry": chain.expiry,
                "strategy": analysis.suggested_strategy,
                "confidence": analysis.confidence,
                "pcr": analysis.pcr,
                "max_pain": analysis.max_pain,
                "strongest_support": analysis.strongest_support,
                "strongest_resistance": analysis.strongest_resistance,
                "reasons": analysis.reasons,
                "trade": trade,
                "entry_validation": validation,
                "rejection": rejection,
            })
        except TokenException as exc:
            return {"available": False, "error_type": "AUTHENTICATION",
                    "rejection": {"code": "AUTHENTICATION_FAILED", "category": "DATA", "reason": f"Kite token error: {exc}"},
                    "reason": f"Kite token error: {exc}", "reasons": []}
        except RequestException as exc:
            return {"available": False, "error_type": "NETWORK",
                    "rejection": {"code": "NETWORK_FAILED", "category": "DATA", "reason": f"Kite network error: {exc}"},
                    "reason": f"Kite network error: {exc}", "reasons": []}
        except ValueError as exc:
            return {"available": False, "error_type": "OPTION_DATA",
                    "rejection": {"code": "OPTION_DATA_INVALID", "category": "DATA", "reason": str(exc)},
                    "reason": str(exc), "reasons": []}
        except Exception as exc:
            return {"available": False, "error_type": exc.__class__.__name__,
                    "rejection": {"code": "OPTION_PROVIDER_ERROR", "category": "DATA", "reason": repr(exc)},
                    "reason": repr(exc), "reasons": []}

    def _historical_context(self, symbol: str) -> dict[str, Any]:
        try:
            history = self.provider.get_long_history(symbol, period="10y")
            return {"current_month": CurrentMonthSeasonality.analyze(history),
                    "regime": RegimePerformance.analyze(history, "BULLISH")}
        except Exception as exc:
            reason = f"{exc.__class__.__name__}: {exc}"
            return {"current_month": CurrentMonthSeasonality.unavailable(
                        date.today().strftime("%B").upper(), reason),
                    "regime": {"available": False, "regime": "UNAVAILABLE",
                               "sample_count": 0, "reason": reason}}

    def paper_trade(self, symbol: str, side: str, quantity: int | None = None) -> dict[str, Any]:
        side = side.strip().upper() if isinstance(side, str) else ""
        if side not in {"BUY", "SELL"}:
            raise ValidationError("side must be BUY or SELL")
        analysis = self.analyze(symbol)
        suggested_quantity = analysis["position_size"]["quantity"]
        quantity = suggested_quantity if quantity is None else quantity
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValidationError("quantity must be a positive integer")
        try:
            return self.paper_broker.place_order(
                analysis["symbol"], side, quantity, price=analysis["analysis"]["current_price"]
            )
        except ValueError as exc:
            raise OrderError(str(exc)) from exc

    def portfolio(self) -> dict[str, Any]:
        return self._serialize(self.paper_broker.portfolio())

    def daily_report(self, limit: int = 15, minimum_score: int = 40) -> dict[str, Any]:
        """Generate the final ranked daily trade report.

        This is a research/paper-trading recommendation only.  It never sends
        live orders, even when Kite is the configured data source.
        """
        if not isinstance(limit, int) or not 1 <= limit <= 15:
            raise ValidationError("limit must be an integer between 1 and 15")
        if not isinstance(minimum_score, int) or not 0 <= minimum_score <= 100:
            raise ValidationError("minimum_score must be an integer between 0 and 100")
        return self._serialize(DailyTradingAssistant(self).generate(limit, minimum_score))

    def record_trade_outcome(self, recommendation_id: str, won: bool, return_percent: float | None = None) -> dict[str, Any]:
        if not isinstance(recommendation_id, str) or not recommendation_id:
            raise ValidationError("recommendation_id is required")
        if not isinstance(won, bool):
            raise ValidationError("won must be true or false")
        if return_percent is not None and not isinstance(return_percent, (int, float)):
            raise ValidationError("return_percent must be numeric")
        saved = OutcomeRepository().record_outcome(recommendation_id, won, return_percent)
        if not saved:
            raise ValidationError("recommendation_id was not found")
        return {"recommendation_id": recommendation_id, "recorded": True}
