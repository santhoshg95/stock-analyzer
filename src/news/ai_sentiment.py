"""Free, local financial sentiment using FinBERT and spaCy."""

from __future__ import annotations

import os
from statistics import mean
from threading import RLock
from typing import Any


class AISentimentError(RuntimeError):
    """Raised when local NLP models cannot produce a trustworthy result."""


class AISentimentAnalyzer:
    """Analyze financial text locally; no paid API or sentiment lexicon."""

    def __init__(self, model: str | None = None, spacy_model: str | None = None,
                 sentiment_pipeline=None, nlp=None):
        self.model = model or os.getenv("NEWS_FINBERT_MODEL", "ProsusAI/finbert")
        self.spacy_model = spacy_model or os.getenv("NEWS_SPACY_MODEL", "en_core_web_sm")
        self._sentiment_pipeline = sentiment_pipeline
        self._nlp = nlp
        self._model_lock = RLock()

    def _load(self) -> None:
        with self._model_lock:
            if self._sentiment_pipeline is None:
                try:
                    from transformers import pipeline
                    self._sentiment_pipeline = pipeline(
                        "text-classification", model=self.model, tokenizer=self.model,
                    )
                except (ImportError, OSError, RuntimeError) as exc:
                    raise AISentimentError(
                        "FinBERT is unavailable. Install requirements and download the configured NEWS_FINBERT_MODEL."
                    ) from exc
            if self._nlp is None:
                try:
                    import spacy
                    self._nlp = spacy.load(self.spacy_model)
                except (ImportError, OSError) as exc:
                    raise AISentimentError(
                        f"spaCy model {self.spacy_model!r} is unavailable; run: python -m spacy download {self.spacy_model}"
                    ) from exc

    @staticmethod
    def _probabilities(raw_result) -> dict[str, float]:
        rows = raw_result
        while isinstance(rows, list) and len(rows) == 1 and isinstance(rows[0], list):
            rows = rows[0]
        if not isinstance(rows, list):
            raise AISentimentError("FinBERT returned an invalid classification payload")
        probabilities = {str(row["label"]).lower(): float(row["score"]) for row in rows}
        if not {"positive", "negative", "neutral"}.issubset(probabilities):
            raise AISentimentError("FinBERT response is missing sentiment probabilities")
        return probabilities

    @staticmethod
    def _label(score: float) -> str:
        return "BULLISH" if score >= 15 else "BEARISH" if score <= -15 else "NEUTRAL"

    def analyze(self, symbol: str, articles: list[dict[str, Any]]) -> dict[str, Any]:
        self._load()
        assessments, signed_scores, confidences, all_entities = [], [], [], []
        # The shared transformers/spaCy objects are reused across requests and
        # guarded because concurrent model inference is not reliably thread-safe.
        with self._model_lock:
            for article in articles:
                text = " ".join(filter(None, (article.get("title"), article.get("description"))))
                if not text.strip():
                    continue
                probabilities = self._probabilities(
                    self._sentiment_pipeline(text, top_k=None, truncation=True)
                )
                signed_score = (probabilities["positive"] - probabilities["negative"]) * 100
                label = self._label(signed_score)
                confidence = max(probabilities.values()) * 100
                doc = self._nlp(text)
                entities = [
                    {"text": entity.text, "label": entity.label_}
                    for entity in doc.ents if entity.text.strip()
                ]
                all_entities.extend(entities)
                materiality = "HIGH" if abs(signed_score) >= 60 and confidence >= 70 else "MEDIUM" if abs(signed_score) >= 30 else "LOW"
                assessments.append({
                    "title": str(article.get("title", "")), "sentiment": label,
                    "materiality": materiality,
                    "summary": f"FinBERT {label.lower()} probability assessment; {len(entities)} entities extracted.",
                    "probabilities": {key: round(value * 100, 2) for key, value in probabilities.items()},
                    "entities": entities,
                })
                signed_scores.append(signed_score)
                confidences.append(confidence)
        if not assessments:
            raise AISentimentError("No usable article text was available for local AI analysis")

        score = mean(signed_scores)
        confidence = mean(confidences)
        sentiment = self._label(score)
        materiality = "HIGH" if abs(score) >= 60 and confidence >= 70 else "MEDIUM" if abs(score) >= 30 else "LOW"
        trade_impact = (
            "BLOCK" if sentiment == "BEARISH" and materiality == "HIGH"
            else "CAUTION" if sentiment == "BEARISH"
            else "SUPPORTIVE" if sentiment == "BULLISH"
            else "NONE"
        )
        return {
            "sentiment": sentiment, "score": round(score, 2),
            "confidence": round(confidence, 2), "materiality": materiality,
            "events": [],
            "reasoning": [
                f"FinBERT analyzed {len(assessments)} financial news items locally.",
                f"Average signed sentiment score is {score:.2f}; article confidence averages {confidence:.2f}%.",
                f"spaCy extracted {len(all_entities)} named entities for report context.",
            ],
            "trade_impact": trade_impact, "article_assessments": assessments,
            "entities": all_entities, "analysis_provider": "LOCAL_FINBERT_SPACY",
        }
