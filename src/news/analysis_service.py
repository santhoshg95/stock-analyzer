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

from src.news.ai_sentiment import AISentimentAnalyzer, AISentimentError


class NewsAnalysisService:
    """Fetch news and delegate all semantic interpretation to an AI model."""

    @staticmethod
    def _text(value: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", unescape(value or ""))).strip()

    @classmethod
    def analyze(cls, symbol: str, timeout: float = 4.0, limit: int = 8,
                analyzer: AISentimentAnalyzer | None = None) -> dict[str, Any]:
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
                "sentiment": "NEUTRAL",
                "confidence": 0,
                "article_count": 0,
                "events": [],
                "headlines": [],
                "reasons": [f"News feed unavailable: {exc.__class__.__name__}."],
                "analysis_method": "UNAVAILABLE",
                "score_impact": 0,
            }

        articles = []
        for item in root.findall("./channel/item")[:limit]:
            title = cls._text(item.findtext("title", ""))
            description = cls._text(item.findtext("description", ""))
            articles.append({
                "title": title,
                "description": description,
                "source": cls._text(item.findtext("source", "Google News")),
                "published": cls._published(item.findtext("pubDate", "")),
            })

        count = len(articles)
        if not articles:
            return {"available": False, "score": 0, "sentiment": "NEUTRAL", "confidence": 0,
                    "article_count": 0, "events": [], "headlines": [], "materiality": "NONE",
                    "trade_impact": "NONE", "analysis_method": "UNAVAILABLE", "score_impact": 0,
                    "reasons": ["No news articles were available for AI analysis; score impact is neutral."]}
        ai_analyzer = analyzer or AISentimentAnalyzer()
        try:
            assessment = ai_analyzer.analyze(symbol, articles)
        except AISentimentError as exc:
            return {"available": False, "score": 0, "sentiment": "NEUTRAL", "confidence": 0,
                    "article_count": count, "events": [], "headlines": articles[:3],
                    "materiality": "NONE", "trade_impact": "NONE",
                    "score_impact": 0,
                    "reasons": [f"{exc} Score impact is neutral."], "analysis_method": "AI_UNAVAILABLE"}
        return {
            "available": True,
            "score": round(float(assessment["score"]), 2),
            "sentiment": assessment["sentiment"],
            "confidence": round(float(assessment["confidence"]), 2),
            "article_count": count,
            "events": assessment["events"],
            "headlines": articles[:3],
            "materiality": assessment["materiality"],
            "trade_impact": assessment["trade_impact"],
            "reasons": assessment["reasoning"],
            "article_assessments": assessment["article_assessments"],
            "entities": assessment.get("entities", []),
            "analysis_method": assessment.get("analysis_provider", "LOCAL_AI_MODEL"),
            "model": ai_analyzer.model,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }

    @staticmethod
    def _published(value: str) -> str | None:
        try:
            return parsedate_to_datetime(value).isoformat()
        except (TypeError, ValueError):
            return None
