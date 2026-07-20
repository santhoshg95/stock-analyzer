"""Candlestick pattern detection with transparent pattern strength.

Strength combines the intrinsic reliability of the pattern (base score) with
available volume and trend confirmation.  It is a confirmation signal, never a
stand-alone reason to trade.
"""

from __future__ import annotations

import pandas as pd


class PatternDetector:
    @staticmethod
    def _candle(row):
        open_, close, high, low = (float(row[key]) for key in ("Open", "Close", "High", "Low"))
        body, span = abs(close - open_), max(high - low, 0.000001)
        return {"open": open_, "close": close, "high": high, "low": low, "body": body,
                "span": span, "upper": high - max(open_, close), "lower": min(open_, close) - low,
                "bull": close > open_, "bear": close < open_}

    @staticmethod
    def _result(pattern: str, base: int, signal: str, current, row) -> dict:
        confirmations = []
        strength = base
        rvol = float(row.get("RVOL", 0) or 0)
        if rvol >= 1.5:
            strength += 10
            confirmations.append("high relative volume")
        elif rvol >= 1:
            strength += 5
            confirmations.append("normal relative volume")
        if current["body"] / current["span"] >= 0.6:
            strength += 5
            confirmations.append("strong candle body")
        return {"pattern": pattern, "strength": min(100, strength), "signal": signal,
                "base_strength": base, "confirmations": confirmations}

    @classmethod
    def detect(cls, df: pd.DataFrame) -> dict:
        if len(df) < 2:
            return {"pattern": "UNKNOWN", "strength": 0, "signal": "NONE", "confirmations": []}
        first = cls._candle(df.iloc[-3]) if len(df) >= 3 else None
        prev, curr = cls._candle(df.iloc[-2]), cls._candle(df.iloc[-1])
        row = df.iloc[-1]

        # Three-candle reversals have priority over one/two-candle patterns.
        if first and first["bear"] and first["body"] > first["span"] * .45 and prev["body"] < first["body"] * .45 and curr["bull"] and curr["close"] > (first["open"] + first["close"]) / 2:
            return cls._result("MORNING STAR", 92, "BUY", curr, row)
        if first and first["bull"] and first["body"] > first["span"] * .45 and prev["body"] < first["body"] * .45 and curr["bear"] and curr["close"] < (first["open"] + first["close"]) / 2:
            return cls._result("EVENING STAR", 92, "SELL", curr, row)

        if prev["bear"] and curr["bull"] and curr["open"] <= prev["close"] and curr["close"] >= prev["open"]:
            return cls._result("BULLISH ENGULFING", 90, "BUY", curr, row)
        if prev["bull"] and curr["bear"] and curr["open"] >= prev["close"] and curr["close"] <= prev["open"]:
            return cls._result("BEARISH ENGULFING", 90, "SELL", curr, row)
        if prev["bear"] and curr["bull"] and curr["open"] < prev["close"] and curr["close"] > (prev["open"] + prev["close"]) / 2:
            return cls._result("PIERCING LINE", 78, "BUY", curr, row)
        if prev["bull"] and curr["bear"] and curr["open"] > prev["close"] and curr["close"] < (prev["open"] + prev["close"]) / 2:
            return cls._result("DARK CLOUD COVER", 78, "SELL", curr, row)
        if prev["bear"] and curr["bull"] and curr["open"] >= prev["close"] and curr["close"] <= prev["open"]:
            return cls._result("BULLISH HARAMI", 70, "BUY", curr, row)
        if prev["bull"] and curr["bear"] and curr["open"] <= prev["close"] and curr["close"] >= prev["open"]:
            return cls._result("BEARISH HARAMI", 70, "SELL", curr, row)

        if curr["body"] / curr["span"] <= .1:
            return cls._result("DOJI", 55, "NEUTRAL", curr, row)
        if curr["lower"] >= curr["body"] * 2 and curr["upper"] <= max(curr["body"], curr["span"] * .12):
            return cls._result("HAMMER" if curr["bull"] else "HANGING MAN", 80, "BUY" if curr["bull"] else "SELL", curr, row)
        if curr["upper"] >= curr["body"] * 2 and curr["lower"] <= max(curr["body"], curr["span"] * .12):
            return cls._result("SHOOTING STAR" if curr["bear"] else "INVERTED HAMMER", 80, "SELL" if curr["bear"] else "BUY", curr, row)
        if curr["body"] / curr["span"] >= .85:
            return cls._result("BULLISH MARUBOZU" if curr["bull"] else "BEARISH MARUBOZU", 75, "BUY" if curr["bull"] else "SELL", curr, row)
        return {"pattern": "NONE", "strength": 0, "signal": "NONE", "confirmations": []}
