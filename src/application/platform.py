"""The supported, safe entry point for analysis, backtesting, and paper trading."""

from __future__ import annotations

from dataclasses import asdict, is_dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import re
from time import sleep
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
from src.trade_plan.trade_plan import TradePlanEngine
from src.trading_engine.engine import TradingEngine


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

        def evaluate(symbol: str) -> dict[str, Any] | None:
            try:
                report = self.analyze(symbol)
            except (DataUnavailableError, ValueError, KeyError, TypeError):
                return None
            analysis = report["analysis"]
            decision = report["decision"]
            if analysis["score"] < minimum_score or decision["action"] not in {"BUY", "BUY ON DIP", "WATCH"}:
                return None
            return {
                "symbol": symbol,
                "action": decision["action"],
                "confidence": decision["confidence"],
                "technical_score": analysis["score"],
                "recommendation": analysis["recommendation"],
                "current_price": analysis["current_price"],
                "risk_reward": report["trade_plan"]["risk_reward"],
                "candlestick": report["candlestick"],
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
                item["risk_reward"],
            ),
            reverse=True,
        )
        top_candidates = candidates[:limit]
        for candidate in top_candidates:
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
            "message": (
                "No stocks currently meet the selected criteria."
                if not candidates
                else f"Ranked candidates using {self.settings.market_data_source} daily data."
            ),
        }

    def _option_trade_plan(self, candidate: dict[str, Any]) -> dict[str, Any]:
        """Enrich only final candidates with live option-chain intelligence."""
        if self.settings.market_data_source != "kite":
            return {"available": False, "reason": "Option analysis requires MARKET_DATA_SOURCE=kite."}
        try:
            chain = KiteOptionChainProvider(self.provider.provider.kite).get_chain(
                candidate["symbol"], candidate["current_price"]
            )
            analysis = OptionEngine().analyze(chain)
            contracts = chain.calls if candidate["action"] in {"BUY", "BUY ON DIP"} else chain.puts
            selected = min(contracts, key=lambda item: abs(item.strike - chain.spot_price)) if contracts else None
            return self._serialize({
                "available": True,
                "expiry": chain.expiry,
                "strategy": analysis.suggested_strategy,
                "confidence": analysis.confidence,
                "pcr": analysis.pcr,
                "max_pain": analysis.max_pain,
                "strongest_support": analysis.strongest_support,
                "strongest_resistance": analysis.strongest_resistance,
                "selected_contract": selected,
                "reasons": analysis.reasons,
            })
        except (TokenException, RequestException, ValueError) as exc:
            return {"available": False, "reason": str(exc), "reasons": []}

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
