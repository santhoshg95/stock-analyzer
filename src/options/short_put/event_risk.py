from __future__ import annotations

from datetime import date


class ShortPutEventRiskEvaluator:
    """Evaluate injected corporate events and news without assuming missing data is safe."""

    MAJOR_TYPES = {"EARNINGS", "RESULTS", "CORPORATE_ACTION", "REGULATORY", "MAJOR_EVENT"}

    @classmethod
    def evaluate(cls, expiry: str, news: dict, corporate_events: list[dict] | None = None) -> dict:
        expiry_date = date.fromisoformat(expiry)
        confirmed = []
        for event in corporate_events or []:
            try:
                event_date = date.fromisoformat(str(event.get("date")))
            except (TypeError, ValueError):
                continue
            if date.today() <= event_date <= expiry_date and str(event.get("type", "")).upper() in cls.MAJOR_TYPES:
                confirmed.append(event)
        if news.get("events"):
            confirmed.extend({"type": item, "source": "NEWS"} for item in news["events"])
        return {
            "available": corporate_events is not None,
            "confirmed_risk": bool(confirmed),
            "events": confirmed,
            "status": "EVENT_RISK" if confirmed else "CLEAR" if corporate_events is not None else "EVENT_DATA_UNAVAILABLE",
        }
