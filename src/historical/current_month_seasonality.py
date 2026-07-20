"""Calendar-month seasonality and current month-to-date comparison."""

from __future__ import annotations

from datetime import date
import calendar

import pandas as pd


class CurrentMonthSeasonality:
    @staticmethod
    def analyze(dataframe: pd.DataFrame, as_of: date | None = None) -> dict:
        as_of = as_of or date.today()
        month = as_of.month
        month_name = calendar.month_name[month].upper()
        if dataframe is None or dataframe.empty:
            return CurrentMonthSeasonality.unavailable(month_name, "No historical data is available.")

        df = dataframe.copy()
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
            df = df.set_index("Date")
        else:
            df.index = pd.to_datetime(df.index, errors="coerce")
        if "Close" not in df.columns:
            return CurrentMonthSeasonality.unavailable(month_name, "Historical data has no Close column.")
        close = pd.to_numeric(df["Close"], errors="coerce").dropna().sort_index()
        close = close[~close.index.duplicated(keep="last")]
        if close.empty:
            return CurrentMonthSeasonality.unavailable(month_name, "Historical closing prices are invalid.")

        monthly_close = close.resample("ME").last()
        monthly_returns = monthly_close.pct_change()
        completed = monthly_returns[
            (monthly_returns.index.month == month) & (monthly_returns.index.year < as_of.year)
        ].dropna()

        current = close[(close.index.year == as_of.year) & (close.index.month == month)]
        previous = close[close.index < pd.Timestamp(as_of.year, month, 1)]
        mtd = None
        if not current.empty and not previous.empty and previous.iloc[-1] > 0:
            mtd = float(current.iloc[-1] / previous.iloc[-1] - 1)

        sample_count = len(completed)
        average = float(completed.mean()) if sample_count else None
        median = float(completed.median()) if sample_count else None
        win_rate = float((completed > 0).mean() * 100) if sample_count else None
        comparison = "UNAVAILABLE"
        if mtd is not None and average is not None:
            comparison = "OUTPERFORMING" if mtd > average else "UNDERPERFORMING" if mtd < average else "IN_LINE"
        quality = "ROBUST" if sample_count >= 8 else "LIMITED" if sample_count >= 5 else "INSUFFICIENT"
        score = 50.0
        if average is not None and win_rate is not None:
            score = max(0, min(100, 50 + average * 500 + (win_rate - 50) * .4))

        return {
            "available": sample_count > 0, "month": month, "month_name": month_name,
            "requested_years": 10, "sample_years": sample_count, "sample_quality": quality,
            "history_start": close.index.min().date().isoformat(),
            "history_end": close.index.max().date().isoformat(),
            "average_return_percent": round(average * 100, 2) if average is not None else None,
            "median_return_percent": round(median * 100, 2) if median is not None else None,
            "win_rate_percent": round(win_rate, 2) if win_rate is not None else None,
            "positive_years": int((completed > 0).sum()), "negative_years": int((completed < 0).sum()),
            "best_return_percent": round(float(completed.max()) * 100, 2) if sample_count else None,
            "worst_return_percent": round(float(completed.min()) * 100, 2) if sample_count else None,
            "current_mtd_return_percent": round(mtd * 100, 2) if mtd is not None else None,
            "versus_history": comparison, "score": round(score, 2),
            "yearly_returns_percent": {str(index.year): round(float(value) * 100, 2)
                                        for index, value in completed.items()},
        }

    @staticmethod
    def unavailable(month_name: str, reason: str) -> dict:
        return {"available": False, "month_name": month_name, "requested_years": 10,
                "sample_years": 0, "sample_quality": "INSUFFICIENT", "score": 50,
                "reason": reason, "current_mtd_return_percent": None,
                "versus_history": "UNAVAILABLE"}
