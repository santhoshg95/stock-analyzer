"""Two-stage setup detection and entry confirmation."""

from __future__ import annotations

import pandas as pd


class SetupEntryEvaluator:
    @staticmethod
    def evaluate(df: pd.DataFrame, analysis, entry: dict, breakout: dict,
                 candlestick: dict) -> dict:
        latest = df.iloc[-1]
        close = float(latest["Close"])
        ema20, ema50, ema200 = (float(latest[name]) for name in ("EMA20", "EMA50", "EMA200"))
        rsi = float(latest["RSI"])
        macd, macd_signal = float(latest["MACD"]), float(latest["MACD_SIGNAL"])
        rvol = float(latest["RVOL"])
        support = entry.get("support")
        support_nearby = bool(support and close > 0 and 0 <= (close - support) / close <= .04)

        lows = pd.to_numeric(df["Low"], errors="coerce").dropna()
        higher_low = False
        if len(lows) >= 8:
            prior_swing_low = float(lows.iloc[-8:-4].min())
            recent_swing_low = float(lows.iloc[-4:].min())
            higher_low = recent_swing_low > prior_swing_low

        bullish_candle = candlestick.get("signal") == "BUY"
        macd_above_signal = macd > macd_signal
        volume_expansion = rvol >= 1.2
        above_ema20 = close > ema20
        bullish_stack = close > ema20 > ema50 > ema200
        long_trend_intact = ema50 > ema200 and close > ema200

        if breakout.get("confirmed"):
            category = "BREAKOUT"
        elif bullish_stack and macd_above_signal:
            category = "TREND FOLLOWING"
        elif rsi < 35 and (macd_above_signal or float(latest.get("MACD_HISTOGRAM", 0)) > 0) and support_nearby:
            category = "REVERSAL CANDIDATE"
        elif long_trend_intact and close <= ema20 and support_nearby:
            category = "PULLBACK"
        elif analysis.score >= 55:
            category = "WATCHLIST"
        else:
            category = "REJECT"

        confirmation_checks = {
            "price_above_ema20": above_ema20,
            "bullish_reversal_candle": bullish_candle,
            "higher_low": higher_low,
            "volume_above_1_2x": volume_expansion,
            "macd_above_signal": macd_above_signal,
        }
        if category == "BREAKOUT":
            confirmation_checks["resistance_broken"] = bool(breakout.get("confirmed"))

        eligible = category != "REJECT" and all(confirmation_checks.values())
        setup_evidence = {
            "oversold_rsi": rsi < 35,
            "macd_turning_up": macd_above_signal,
            "support_nearby": support_nearby,
            "risk_reward_at_least_1_5": (entry.get("risk_reward") or 0) >= 1.5,
            "long_trend_intact": long_trend_intact,
        }
        return {
            "stage_1": {"detected": category != "REJECT", "category": category,
                        "evidence": setup_evidence},
            "stage_2": {"eligible": eligible, "status": "TRADE_ELIGIBLE" if eligible else "WAIT",
                        "checks": confirmation_checks,
                        "missing": [name for name, passed in confirmation_checks.items() if not passed]},
            "momentum_label": ("EARLY_REVERSAL" if rsi < 35 and macd_above_signal
                               else "STRONG_BULLISH" if bullish_stack and volume_expansion and higher_low
                               else "BULLISH" if above_ema20 and macd_above_signal else "BEARISH"),
        }
