"""Reliable, dependency-light news collection and sentiment analysis.

News is intentionally evaluated only after technical screening has produced a
small shortlist.  A failed feed must never block a trading report.
"""

from __future__ import annotations

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from html import unescape
import re
from typing import Any
from urllib.parse import quote_plus
from xml.etree import ElementTree

import requests


class NewsAnalysisService:
    """Fetch recent Google News RSS headlines and return an explainable score."""

    POSITIVE = {
        "beat", "beats", "approval", "approved", "growth", "profit", "profits",
        "upgrade", "upgraded", "order", "orders", "contract", "record", "surge",
        "rally", "bullish", "buyback", "dividend", "expansion", "strong",
    }
    NEGATIVE = {
        "miss", "misses", "loss", "losses", "downgrade", "downgraded", "fraud",
        "probe", "penalty", "default", "recall", "warning", "fall", "falls",
        "plunge", "bearish", "lawsuit", "resigns", "resignation", "weak",
    }
    HIGH_RISK = {"fraud", "probe", "penalty", "default", "recall", "lawsuit", "resigns", "resignation"}

    @staticmethod
    def _text(value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(value or ""))).strip()

    @classmethod
    def _article_score(cls, text: str) -> tuple[int, list[str]]:
        words = set(re.findall(r"[a-z]+", text.lower()))
        positive, negative = len(words & cls.POSITIVE), len(words & cls.NEGATIVE)
        events = sorted(words & cls.HIGH_RISK)
        score = positive - negative - (2 * len(events))
        return score, events

    @classmethod
    def analyze(cls, symbol: str, timeout: float = 4.0, limit: int = 8) -> dict[str, Any]:
        """Return a bounded sentiment/event assessment for a stock symbol."""
        url = "https://news.google.com/rss/search?q=" + quote_plus(f"{symbol} NSE stock") + "&hl=en-IN&gl=IN&ceid=IN:en"
        try:
            response = requests.get(url, timeout=timeout, headers={"User-Agent": "stock-analyzer/1.0"})
            response.raise_for_status()
            root = ElementTree.fromstring(response.content)
        except (requests.RequestException, ElementTree.ParseError) as exc:
            return {
                "available": False,
                "score": 0,
                "sentiment": "UNAVAILABLE",
                "confidence": 0,
                "article_count": 0,
                "events": [],
                "headlines": [],
                "reasons": [f"News feed unavailable: {exc.__class__.__name__}."],
            }

        articles, total, events = [], 0, set()
        for item in root.findall("./channel/item")[:limit]:
            title = cls._text(item.findtext("title", ""))
            description = cls._text(item.findtext("description", ""))
            score, article_events = cls._article_score(f"{title} {description}")
            total += score
            events.update(article_events)
            articles.append({
                "title": title,
                "source": cls._text(item.findtext("source", "Google News")),
                "published": cls._published(item.findtext("pubDate", "")),
                "sentiment_score": score,
            })

        count = len(articles)
        normalized = round(max(-100, min(100, (total / max(count, 1)) * 25)), 2)
        sentiment = "BULLISH" if normalized >= 15 else "BEARISH" if normalized <= -15 else "NEUTRAL"
        confidence = min(80, count * 10)
        reasons = [f"News sentiment is {sentiment.lower()} ({normalized:+.1f})."]
        if events:
            reasons.append("Risk events detected: " + ", ".join(sorted(events)) + ".")
        return {
            "available": True,
            "score": normalized,
            "sentiment": sentiment,
            "confidence": confidence,
            "article_count": count,
            "events": sorted(events),
            "headlines": articles[:3],
            "reasons": reasons,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _published(value: str) -> str | None:
        try:
            return parsedate_to_datetime(value).isoformat()
        except (TypeError, ValueError):
            return None
