"""Optional FastAPI adapter for :class:`src.application.TradingPlatform`."""

try:
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
except ImportError as exc:  # Keeps importing the analysis package dependency-light.
    raise RuntimeError("REST API requires fastapi; install requirements.txt first") from exc

from src.application.errors import PlatformError
from src.application.platform import TradingPlatform

app = FastAPI(title="AI Quantitative Trading Platform", version="1.0.0")
platform = TradingPlatform()


class SymbolRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=30)


class PaperTradeRequest(SymbolRequest):
    side: str
    quantity: int | None = Field(default=None, gt=0)


def _call(operation):
    try:
        return operation()
    except PlatformError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "paper"}


@app.post("/analyze")
def analyze(request: SymbolRequest):
    return _call(lambda: platform.analyze(request.symbol))


@app.get("/suggestions")
def suggestions(limit: int = 5, minimum_score: int = 40):
    return _call(lambda: platform.suggest_stocks(limit, minimum_score))


@app.post("/backtest")
def backtest(request: SymbolRequest):
    return _call(lambda: platform.backtest(request.symbol))


@app.post("/papertrade")
def paper_trade(request: PaperTradeRequest):
    return _call(lambda: platform.paper_trade(request.symbol, request.side, request.quantity))


@app.get("/portfolio")
def portfolio():
    return platform.portfolio()
