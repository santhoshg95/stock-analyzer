"""Persistent recommendation and outcome store for probability calibration."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


class OutcomeRepository:
    def __init__(self, path: str | Path = "data/cache/trades/outcomes.json"):
        self.path = Path(path)

    def _read(self) -> list[dict[str, Any]]:
        try:
            return json.loads(self.path.read_text())
        except (OSError, json.JSONDecodeError):
            return []

    def _write(self, rows: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(rows, indent=2))

    def record_recommendation(self, trade: dict[str, Any]) -> str:
        rows = self._read()
        identifier = f"{trade['symbol']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        rows.append({"id": identifier, "created_at": datetime.now(timezone.utc).isoformat(),
                     "symbol": trade["symbol"], "strategy": trade["strategy"],
                     "ai_score": trade["ai_score"], "estimated_probability": trade["probability"],
                     "outcome": None})
        self._write(rows)
        return identifier

    def record_outcome(self, identifier: str, won: bool, return_percent: float | None = None) -> bool:
        rows = self._read()
        for row in rows:
            if row["id"] == identifier:
                row.update({"outcome": "WIN" if won else "LOSS", "return_percent": return_percent,
                            "closed_at": datetime.now(timezone.utc).isoformat()})
                self._write(rows)
                return True
        return False

    def calibrated_probability(self, strategy: str, minimum_samples: int = 20) -> float | None:
        rows = [row for row in self._read() if row.get("strategy") == strategy and row.get("outcome") in {"WIN", "LOSS"}]
        if len(rows) < minimum_samples:
            return None
        return round(sum(row["outcome"] == "WIN" for row in rows) * 100 / len(rows), 2)
