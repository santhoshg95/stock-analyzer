"""Historical forward performance conditioned on a simple price regime."""

from __future__ import annotations

import pandas as pd


class RegimePerformance:
    @staticmethod
    def analyze(dataframe: pd.DataFrame, direction: str = "BULLISH") -> dict:
        if dataframe is None or dataframe.empty:
            return {"available": False, "regime": "UNAVAILABLE", "sample_count": 0,
                    "reason": "No historical data is available."}
        df = dataframe.copy()
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.set_index("Date")
        else:
            df.index = pd.to_datetime(df.index, errors="coerce")
        close = pd.to_numeric(df.get("Close"), errors="coerce").dropna().sort_index()
        if len(close) < 220:
            return {"available": False, "regime": "UNAVAILABLE", "sample_count": 0,
                    "reason": "At least 220 valid daily closes are required."}
        frame = pd.DataFrame({"close": close})
        frame["sma50"] = close.rolling(50).mean()
        frame["sma200"] = close.rolling(200).mean()
        frame["forward_return"] = close.shift(-21) / close - 1
        frame["regime"] = "SIDEWAYS"
        frame.loc[(frame.close > frame.sma50) & (frame.sma50 > frame.sma200), "regime"] = "BULL"
        frame.loc[(frame.close < frame.sma50) & (frame.sma50 < frame.sma200), "regime"] = "BEAR"
        current = str(frame.iloc[-1]["regime"])
        # Month-end samples reduce heavy overlap between 21-session outcomes.
        samples = frame.resample("ME").last()
        samples = samples[(samples.regime == current) & samples.forward_return.notna()]
        returns = samples["forward_return"]
        wins = returns > 0 if direction == "BULLISH" else returns < 0
        count = len(returns)
        return {
            "available": count > 0, "regime": current, "direction": direction,
            "sample_count": count, "sample_quality": "ROBUST" if count >= 30 else "LIMITED" if count >= 15 else "INSUFFICIENT",
            "win_rate_percent": round(float(wins.mean()) * 100, 2) if count else None,
            "average_forward_return_percent": round(float(returns.mean()) * 100, 2) if count else None,
            "median_forward_return_percent": round(float(returns.median()) * 100, 2) if count else None,
            "horizon_sessions": 21,
        }
