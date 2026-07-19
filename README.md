# AI Quantitative Trading Platform

An analysis-first trading platform for NSE equities. It uses Zerodha Kite for
historical OHLCV and live quotes, then provides technical analysis, trade
planning, backtesting, and a stateful paper-trading workflow.
Live order placement is intentionally not exposed by the public platform API.

## Quick start

Configure a valid daily Zerodha Kite access token in `.env`, then run:

```env
KITE_API_KEY=your_kite_api_key
KITE_ACCESS_TOKEN=your_daily_access_token
```

```bash
.venv/bin/python main.py analyze RELIANCE
.venv/bin/python main.py suggest --limit 5
.venv/bin/python main.py backtest RELIANCE
.venv/bin/python main.py papertrade RELIANCE BUY --quantity 10
.venv/bin/python main.py portfolio
```

Runtime defaults can be configured without changing source code:

```bash
export TRADING_CAPITAL=100000
export TRADING_RISK_PERCENT=1
export MARKET_DATA_SOURCE=kite
```

## Application API

`TradingPlatform` is the supported integration point for scripts and services:

```python
from src.application import TradingPlatform

platform = TradingPlatform()
suggestions = platform.suggest_stocks(limit=5)
report = platform.analyze("RELIANCE")
backtest = platform.backtest("RELIANCE")
order = platform.paper_trade("RELIANCE", "BUY", quantity=10)
```

Start with `suggest_stocks()` to rank the configured market universe. Candidates
are filtered to actionable BUY, BUY ON DIP, or WATCH setups and include a trade
plan and suggested risk-based quantity. It normalizes symbols, validates
orders, calculates a position size from the configured capital/risk limit, and
raises clear application errors when data is unavailable or input is invalid.

## REST API

Install the dependencies, then start the API:

```bash
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn src.api:app --reload
```

Available endpoints are `GET /health`, `GET /suggestions`, `POST /analyze`, `POST /backtest`,
`POST /papertrade`, and `GET /portfolio`. Request bodies for the first two are
`{"symbol": "RELIANCE"}`; paper trading also accepts `side` and optional
`quantity`.

`MARKET_DATA_SOURCE=cache` is available only as an explicit offline fallback
for development; it is not the default.

The local instrument file is used only to map a symbol such as `RELIANCE` to
Kite's instrument token. Candle/price data used in analysis comes from Kite on
each request.

This project is for research and paper trading. It does not constitute
investment advice.
