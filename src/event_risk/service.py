from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import hashlib
import json
import logging
import math
from pathlib import Path
import re
from time import perf_counter
from typing import Any, Callable

from src.event_risk.models import (
    EventCategory, EventDirection, EventImpactDuration, EventRiskAssessment,
    EventRiskItem, EventSeverity, EventSourceType, EventStatus,
)
from src.event_risk.repository import EventRepository


logger = logging.getLogger(__name__)
SEVERITY_SCORE = {"VERY_LOW": 10, "LOW": 30, "MEDIUM": 50, "HIGH": 75, "EXTREME": 95}


@dataclass
class DailyEventContext:
    events: list[EventRiskItem]
    data_state: str
    warnings: list[str]
    timings: dict[str, float | int]


class EventRiskService:
    """Build shared event context once and assess symbols without changing quality."""

    def __init__(self, settings, repository: EventRepository | None = None,
                 commodity_fetcher: Callable[[], dict[str, Any]] | None = None,
                 config_path: str | Path = "resources/event_risk_config.json"):
        self.settings = settings
        self.repository = repository or EventRepository()
        self.commodity_fetcher = commodity_fetcher
        try:
            self.mapping = json.loads(Path(config_path).read_text())
        except (OSError, json.JSONDecodeError):
            self.mapping = {"company_types": {}, "crude_exposure": {}, "sector_sensitivity": {}}
        self.mapping.setdefault("sector_sensitivity", {}).update(
            self.mapping.get("extended_sector_sensitivity", {})
        )

    @staticmethod
    def _dt(value: Any, fallback: datetime) -> datetime:
        if isinstance(value, datetime):
            result = value
        elif isinstance(value, str):
            try:
                result = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                result = fallback
        else:
            result = fallback
        return result.replace(tzinfo=result.tzinfo or timezone.utc)

    @staticmethod
    def fingerprint(event: EventRiskItem) -> str:
        date_bucket = (event.event_start or event.detected_at).strftime("%Y-%m-%d")
        identity = "|".join((event.normalized_event_type,
                             ",".join(sorted(event.affected_regions)),
                             ",".join(sorted(event.affected_commodities)), date_bucket))
        return hashlib.sha1(identity.encode()).hexdigest()[:16]

    def decay(self, event: EventRiskItem, as_of: datetime) -> tuple[float, float]:
        if event.expiry_time and as_of >= event.expiry_time:
            return 0.0, 0.0
        if event.decay_model == "NO_DECAY_WHILE_ACTIVE" and event.status in {EventStatus.ACTIVE, EventStatus.ESCALATING}:
            return event.raw_score, 1.0
        elapsed = max(0, (as_of - event.last_updated_at).total_seconds() / 3600)
        half_life = max(1, event.half_life_hours)
        if event.status == EventStatus.DE_ESCALATING:
            half_life *= .5
        elif event.status == EventStatus.RESOLVED:
            half_life *= .25
        if event.decay_model == "LINEAR":
            factor = max(0, 1 - elapsed / (half_life * 2))
        elif event.decay_model == "STEP":
            factor = 1.0 if elapsed < half_life else .25
        else:
            factor = math.exp(-math.log(2) * elapsed / half_life)
        if event.status == EventStatus.ESCALATING:
            factor = min(1.15, factor * 1.15)
        return round(event.raw_score * factor, 2), round(factor, 4)

    def _from_row(self, row: dict[str, Any], as_of: datetime,
                  source: EventSourceType = EventSourceType.CACHED_SOURCE) -> EventRiskItem | None:
        if row.get("test_only") and not self.settings.event_allow_test_overrides:
            return None
        event_type = str(row.get("normalized_event_type") or row.get("event_type") or "UNKNOWN").upper()
        severity = str(row.get("severity", "MEDIUM")).upper()
        direction = str(row.get("direction", "UNCERTAIN")).upper()
        status = str(row.get("status", "ACTIVE")).upper()
        detected = self._dt(row.get("detected_at") or row.get("start_time"), as_of)
        updated = self._dt(row.get("last_updated_at") or row.get("start_time"), detected)
        category_name = str(row.get("category") or ("GEOPOLITICAL" if "CONFLICT" in event_type else "COMPANY")).upper()
        event = EventRiskItem(
            event_id=str(row.get("event_id") or hashlib.sha1((event_type + detected.isoformat()).encode()).hexdigest()[:16]),
            title=str(row.get("title") or event_type.replace("_", " ").title()),
            normalized_event_type=event_type,
            category=EventCategory.__members__.get(category_name, EventCategory.COMPANY),
            severity=EventSeverity.__members__.get(severity, EventSeverity.MEDIUM),
            direction=EventDirection.__members__.get(direction, EventDirection.UNCERTAIN),
            status=EventStatus.__members__.get(status, EventStatus.ACTIVE),
            source_type=source,
            detected_at=detected, last_updated_at=updated,
            event_start=self._dt(row.get("event_start") or row.get("start_time"), detected),
            event_end=self._dt(row["event_end"], detected) if row.get("event_end") else None,
            expected_duration=EventImpactDuration.__members__.get(
                str(row.get("expected_duration", "ONE_TO_THREE_DAYS")).upper(),
                EventImpactDuration.ONE_TO_THREE_DAYS),
            raw_score=float(row.get("raw_score", SEVERITY_SCORE.get(severity, 50))),
            confidence=float(row.get("confidence", .7)), materiality=float(row.get("materiality", 1)),
            gap_risk=float(row.get("gap_risk", SEVERITY_SCORE.get(severity, 50) * .8)),
            affected_sectors=[str(x).upper() for x in row.get("affected_sectors", [])],
            affected_symbols=[str(x).upper() for x in row.get("affected_symbols", [])],
            affected_regions=[str(x).upper() for x in row.get("affected_regions", [])],
            affected_commodities=[str(x).upper() for x in row.get("affected_commodities", [])],
            reasons=list(row.get("reasons", [str(row.get("reason", "Event source matched."))])),
            source_titles=list(row.get("source_titles", [])),
            source_urls_or_ids=list(row.get("source_urls_or_ids", [])),
            is_scheduled=bool(row.get("is_scheduled", False)),
            is_confirmed=bool(row.get("is_confirmed", source == EventSourceType.MANUAL_OVERRIDE)),
            half_life_hours=float(row.get("half_life_hours", self._half_life(category_name))),
            decay_model=str(row.get("decay_model", "EXPONENTIAL")).upper(),
            expiry_time=self._dt(row["expiry_time"], detected) if row.get("expiry_time") else None,
        )
        age_minutes = max(0, (as_of - updated).total_seconds() / 60)
        event.freshness_score = (100 if age_minutes <= self.settings.event_data_max_age_minutes
                                 else 60 if age_minutes <= self.settings.event_stale_after_minutes else 25)
        if event.freshness_score < 50 and event.status not in {EventStatus.RESOLVED, EventStatus.STALE}:
            event.status = EventStatus.STALE
        event.decayed_score, _ = self.decay(event, as_of)
        return event if event.decayed_score > 0 else None

    def _half_life(self, category: str) -> float:
        if category == "GEOPOLITICAL":
            return self.settings.geopolitical_half_life_hours
        if category == "EARNINGS":
            return self.settings.earnings_half_life_hours
        if category == "COMMODITY":
            return self.settings.commodity_shock_half_life_hours
        return self.settings.event_default_half_life_hours

    def _commodity_events(self, snapshot: dict[str, Any], as_of: datetime) -> list[EventRiskItem]:
        events = []
        aliases = self.mapping.get("commodity_event_types", {})
        for source_name, base_type in aliases.items():
            data = snapshot.get(source_name) or snapshot.get(source_name.upper()) or {}
            if not isinstance(data, dict):
                continue
            move = float(data.get("one_day_change_pct", data.get("change_percent", 0)) or 0)
            zscore = float(data.get("z_score", 0) or 0)
            multi = float(data.get("three_day_change_pct", 0) or 0)
            significant = (abs(move) >= self.settings.crude_daily_move_warning
                           or abs(zscore) >= self.settings.commodity_zscore_high
                           or abs(multi) >= self.settings.commodity_multiday_move_high)
            if not significant:
                continue
            severity = (EventSeverity.EXTREME if abs(move) >= self.settings.crude_daily_move_extreme
                        or abs(zscore) >= self.settings.commodity_zscore_extreme else
                        EventSeverity.HIGH if abs(move) >= self.settings.crude_daily_move_high else
                        EventSeverity.MEDIUM)
            direction = EventDirection.POSITIVE if move > 0 else EventDirection.NEGATIVE
            raw = max(SEVERITY_SCORE[severity.value], min(100, abs(zscore) * 25))
            normalized_type = base_type + ("_UP" if move > 0 else "_DOWN")
            display_name = source_name.replace("_", " ").title()
            events.append(EventRiskItem(
                event_id=f"{base_type}-{as_of:%Y%m%d}", title=f"{display_name} {move:+.2f}%",
                normalized_event_type=normalized_type, category=EventCategory.COMMODITY,
                severity=severity, direction=direction, source_type=EventSourceType.COMMODITY_DATA,
                detected_at=as_of, last_updated_at=as_of,
                expected_duration=EventImpactDuration.THREE_TO_SEVEN_DAYS,
                raw_score=raw, decayed_score=raw, confidence=.9, gap_risk=min(100, raw * .85),
                affected_sectors=self.mapping.get("commodity_affected_sectors", {}).get(base_type, []),
                affected_commodities=[base_type.removesuffix("_PRICE")], reasons=[
                    f"{display_name} move {move:+.2f}%, z-score {zscore:+.2f}, three-day move {multi:+.2f}%.",
                ], is_confirmed=True, half_life_hours=self.settings.commodity_shock_half_life_hours,
            ))
        return events

    def deduplicate(self, events: list[EventRiskItem]) -> list[EventRiskItem]:
        clusters: dict[str, list[EventRiskItem]] = {}
        for event in events:
            clusters.setdefault(self.fingerprint(event), []).append(event)
        result = []
        for fingerprint, members in clusters.items():
            members.sort(key=lambda item: (item.decayed_score, item.confidence), reverse=True)
            canonical = members[0]
            canonical.canonical_event_id = fingerprint
            canonical.related_article_ids = [item.event_id for item in members]
            canonical.meaningful_update_count = max(0, len(members) - 1)
            if len({item.source_type for item in members}) > 1 or len(members) >= 2:
                canonical.confidence = min(1, canonical.confidence + .1)
                canonical.is_confirmed = True
            for duplicate in members[1:]:
                duplicate.is_duplicate, duplicate.duplicate_of = True, canonical.event_id
            result.append(canonical)
        return result

    def build_daily_context(self, market_context: dict[str, Any] | None = None,
                            as_of: datetime | None = None) -> DailyEventContext:
        started = perf_counter()
        as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
        if not self.settings.event_risk_enabled:
            return DailyEventContext([], "DISABLED", [], {"event_total_seconds": 0,
                                                            "event_sources_requested": 0,
                                                            "events_detected": 0,
                                                            "event_clusters_created": 0})
        events, warnings, sources = [], [], 0
        for row in self.repository.read_events():
            event = self._from_row(row, as_of)
            if event:
                events.append(event)
        overrides = self.repository.read_overrides(as_of)
        sources += 1
        for row in overrides:
            event = self._from_row(row, as_of, EventSourceType.MANUAL_OVERRIDE)
            if event:
                events.append(event)
        for rows, source in ((self.repository.read_company_calendar(), EventSourceType.COMPANY_CALENDAR),
                             (self.repository.read_economic_calendar(), EventSourceType.ECONOMIC_CALENDAR)):
            sources += 1
            for row in rows:
                event = self._from_row(row, as_of, source)
                if event:
                    event.is_scheduled = True
                    events.append(event)
        snapshot = self.repository.read_commodity_snapshot()
        if self.commodity_fetcher:
            sources += 1
            try:
                live = self.commodity_fetcher()
                if live:
                    snapshot = live
            except Exception as exc:
                logger.warning("Event commodity source failed: %s", exc)
                warnings.append(f"Commodity event source failed: {exc.__class__.__name__}")
        events.extend(self._commodity_events(snapshot, as_of))
        regime = str((market_context or {}).get("regime", "")).upper()
        vix = float((market_context or {}).get("vix", 0) or 0)
        if regime in {"CRASH", "EVENT_DRIVEN", "HIGH_VOLATILITY", "STRONG_BEARISH"} or vix >= 25:
            raw = 90 if regime == "CRASH" or vix >= 35 else 70
            events.append(EventRiskItem(
                event_id=f"MARKET-WIDE-{as_of:%Y%m%d}", title=f"Market-wide {regime or 'volatility'} risk",
                normalized_event_type="MARKET_WIDE_STRESS", category=EventCategory.MARKET_WIDE,
                severity=EventSeverity.EXTREME if raw >= 90 else EventSeverity.HIGH,
                direction=EventDirection.VOLATILITY_ONLY, source_type=EventSourceType.MARKET_DATA,
                detected_at=as_of, last_updated_at=as_of, raw_score=raw, decayed_score=raw,
                confidence=.85, gap_risk=raw, reasons=[f"Existing regime {regime}; VIX {vix}."],
                is_confirmed=True, half_life_hours=self.settings.event_default_half_life_hours,
            ))
        raw_count = len(events)
        events = self.deduplicate(events)
        state = "FRESH" if events else "UNAVAILABLE"
        if not events:
            warnings.append("No fresh shared event source was available; one conservative penalty applies.")
        else:
            try:
                self.repository.write_events(
                    [event.to_dict() for event in events
                     if event.source_type != EventSourceType.MANUAL_OVERRIDE], as_of
                )
            except OSError as exc:
                logger.warning("Event cache write failed: %s", exc)
                warnings.append(f"Event cache write failed: {exc.__class__.__name__}")
        timings = {"event_context_fetch_seconds": round(perf_counter() - started, 3),
                   "event_classification_seconds": 0.0,
                   "event_sources_requested": sources, "events_detected": raw_count,
                   "event_clusters_created": len(events)}
        logger.info("Event context: %d raw items, %d clusters, fetch=%.3fs",
                    raw_count, len(events), timings["event_context_fetch_seconds"])
        return DailyEventContext(events, state, warnings, timings)

    def _news_events(self, symbol: str, news: dict[str, Any], as_of: datetime) -> list[EventRiskItem]:
        if news.get("collection_state") != "FETCHED":
            return []
        events = []
        for index, headline in enumerate(news.get("headlines", [])):
            title = str(headline.get("title", ""))
            text = title.lower()
            event_type = category = None
            if any(term in text for term in ("war", "missile", "iran", "sanction", "hormuz", "red sea", "conflict")):
                event_type, category = "GEOPOLITICAL_ESCALATION", EventCategory.GEOPOLITICAL
            elif any(term in text for term in ("quarter result", "quarterly result", "earnings", "q1 result", "q2 result", "q3 result", "q4 result")):
                event_type, category = "EARNINGS", EventCategory.EARNINGS
            elif any(term in text for term in ("regulator", "investigation", "warning letter", "trading halt", "default")):
                event_type, category = "REGULATORY_ACTION", EventCategory.REGULATORY
            if not event_type:
                continue
            severity = EventSeverity.HIGH if category in {EventCategory.GEOPOLITICAL, EventCategory.REGULATORY} else EventSeverity.MEDIUM
            event = EventRiskItem(
                event_id=f"{symbol}-NEWS-{index}-{hashlib.sha1(title.encode()).hexdigest()[:8]}",
                title=title, normalized_event_type=event_type, category=category,
                severity=severity, direction=EventDirection.VOLATILITY_ONLY,
                source_type=EventSourceType.NEWS, detected_at=as_of, last_updated_at=as_of,
                raw_score=SEVERITY_SCORE[severity.value], decayed_score=SEVERITY_SCORE[severity.value],
                confidence=min(1, float(news.get("confidence", 50)) / 100),
                gap_risk=70 if category == EventCategory.EARNINGS else 60,
                affected_symbols=[symbol], source_titles=[title], reasons=[f"News classified as {event_type}."],
                is_confirmed=news.get("analysis_state") == "ANALYZED",
                half_life_hours=self._half_life(category.value),
            )
            events.append(event)
        return events

    def _scheduled_proximity(self, event: EventRiskItem, as_of: datetime) -> float:
        if not event.is_scheduled or not event.event_start:
            return 1.0
        hours = (event.event_start - as_of).total_seconds() / 3600
        if hours < -24:
            return .6
        if hours <= 8:
            return 1.25
        if hours <= 24:
            return 1.15
        if hours <= 72:
            return .9
        if hours <= 168:
            return .5
        return .15

    def assess_candidate(self, candidate: dict[str, Any], context: DailyEventContext,
                         news_context: dict[str, Any] | None = None,
                         market_context: dict[str, Any] | None = None,
                         base_readiness: float = 0,
                         as_of: datetime | None = None) -> EventRiskAssessment:
        started = perf_counter()
        as_of = (as_of or datetime.now(timezone.utc)).astimezone(timezone.utc)
        symbol = str(candidate.get("symbol", "")).upper()
        sector = str(candidate.get("sector", "DIVERSIFIED")).upper()
        company_type = self.mapping.get("company_types", {}).get(symbol, "GENERIC")
        events = self.deduplicate([*context.events, *self._news_events(symbol, news_context or {}, as_of)])
        matched: list[tuple[float, EventRiskItem, EventDirection, float]] = []
        directional_bonus = negative_penalty = 0.0
        for event in events:
            direct = symbol in event.affected_symbols
            sector_match = sector in event.affected_sectors or not event.affected_sectors
            global_event = event.category in {EventCategory.GEOPOLITICAL, EventCategory.MACRO,
                                              EventCategory.MARKET_WIDE, EventCategory.CENTRAL_BANK}
            if event.affected_symbols and not direct:
                continue
            if not direct and not sector_match and not global_event:
                continue
            default_sensitivity = 1.0 if direct else .65 if sector_match else .25 if global_event else .5
            sensitivity = float(self.mapping.get("sector_sensitivity", {}).get(sector, {}).get(
                event.normalized_event_type, default_sensitivity))
            if direct:
                sensitivity = max(1.0, sensitivity)
            direction = event.direction
            exposure = 1.0
            if event.normalized_event_type in {"CRUDE_PRICE_UP", "CRUDE_PRICE_DOWN"}:
                mapping = self.mapping.get("crude_exposure", {}).get(company_type, {})
                direction_name = mapping.get("up_direction" if event.normalized_event_type.endswith("UP") else "down_direction", "MIXED")
                direction = EventDirection.__members__.get(direction_name, EventDirection.MIXED)
                exposure = float(mapping.get("directional_weight", .5))
                sensitivity = max(sensitivity, exposure)
            else:
                company_exposure = self.mapping.get("company_event_exposure", {}).get(
                    company_type, {}).get(event.normalized_event_type)
                if company_exposure:
                    direction = EventDirection.__members__.get(
                        company_exposure.get("direction", "MIXED"), EventDirection.MIXED
                    )
                    exposure = float(company_exposure.get("sensitivity", sensitivity))
                    sensitivity = exposure
                else:
                    sector_direction = self.mapping.get("sector_direction", {}).get(sector, {}).get(
                        event.normalized_event_type
                    )
                    if sector_direction:
                        direction = EventDirection.__members__.get(sector_direction, direction)
            decayed, decay_factor = self.decay(event, as_of)
            proximity = self._scheduled_proximity(event, as_of)
            score = min(100, decayed * sensitivity * event.materiality
                        * max(.35, event.confidence) * (event.freshness_score / 100) * proximity)
            if score < 5:
                continue
            matched.append((score, event, direction, decay_factor))
            if direction == EventDirection.POSITIVE:
                directional_bonus += min(15, score * exposure * .18)
            elif direction == EventDirection.NEGATIVE:
                negative_penalty += min(20, score * exposure * .22)
        matched.sort(key=lambda row: row[0], reverse=True)
        event_score = min(100, sum(score * weight for (score, *_), weight in zip(
            matched[:3], (1.0, .35, .20)))) if matched else 0.0
        gap_score = max((event.gap_risk for _, event, _, _ in matched), default=0)
        volatility_score = max((score for score, event, _, _ in matched
                                if event.category in {EventCategory.GEOPOLITICAL, EventCategory.COMMODITY,
                                                      EventCategory.EARNINGS, EventCategory.MARKET_WIDE}), default=0)
        level = ("EXTREME" if event_score >= self.settings.event_extreme_min else
                 "HIGH" if event_score > self.settings.event_medium_max else
                 "MEDIUM" if event_score > self.settings.event_low_max else
                 "LOW" if event_score > self.settings.event_very_low_max else "VERY_LOW")
        volatility_penalty = {"VERY_LOW": 0, "LOW": 2, "MEDIUM": 8, "HIGH": 18, "EXTREME": 30}[level]
        gap_penalty = round(gap_score * .15, 2) if level in {"HIGH", "EXTREME"} else round(gap_score * .07, 2)
        uncertainty_penalty = 0.0
        data_state = context.data_state
        warnings = list(context.warnings)
        if not matched and data_state == "UNAVAILABLE":
            uncertainty_penalty = self.settings.event_data_unavailable_readiness_penalty
        elif any(event.freshness_score < 50 for event in events):
            data_state = "STALE"
            uncertainty_penalty = self.settings.event_data_stale_readiness_penalty
            warnings.append("One or more event sources are stale.")
        total_penalty = volatility_penalty + gap_penalty + negative_penalty + uncertainty_penalty
        bonus = min(directional_bonus, max(0, total_penalty * .6))
        adjusted = min(100, max(0, base_readiness + bonus - total_penalty))
        multiplier = {"VERY_LOW": 1.0, "LOW": 1.0, "MEDIUM": self.settings.event_medium_position_multiplier,
                      "HIGH": self.settings.event_high_position_multiplier,
                      "EXTREME": self.settings.event_extreme_position_multiplier}[level]
        earnings_today = any(event.category == EventCategory.EARNINGS and event.is_scheduled
                             and event.event_start and abs((event.event_start - as_of).total_seconds()) <= 12 * 3600
                             for _, event, _, _ in matched)
        confirmed_extreme = event_score >= self.settings.event_risk_hard_block_score and any(
            event.is_confirmed and not event.is_scheduled for _, event, _, _ in matched)
        extreme_gap = gap_score >= self.settings.event_gap_risk_hard_block_score and any(
            event.is_confirmed for _, event, _, _ in matched)
        hard_block = bool((earnings_today and self.settings.earnings_same_day_block)
                          or extreme_gap
                          or (confirmed_extreme and self.settings.event_extreme_block_new_trades))
        restrictions = []
        if level in {"HIGH", "EXTREME"} and self.settings.event_defined_risk_options_only_at_high:
            restrictions.extend(["DEFINED_RISK_ONLY", "BLOCK_SHORT_PREMIUM", "REDUCE_LOTS"])
        if level in {"HIGH", "EXTREME"}:
            restrictions.extend(["INTRADAY_ONLY", "NO_OVERNIGHT"])
        overnight = not (earnings_today or gap_score >= 60
                          or (level == "EXTREME" and self.settings.event_extreme_block_overnight))
        if not overnight and "NO_OVERNIGHT" not in restrictions:
            restrictions.append("NO_OVERNIGHT")
        directions = {direction for _, _, direction, _ in matched}
        if EventDirection.POSITIVE in directions and level in {"HIGH", "EXTREME"}:
            event_direction = "POSITIVE_BUT_VOLATILE"
        elif EventDirection.NEGATIVE in directions:
            event_direction = "NEGATIVE"
        elif EventDirection.POSITIVE in directions:
            event_direction = "POSITIVE"
        elif matched:
            event_direction = "VOLATILITY_ONLY" if directions == {EventDirection.VOLATILITY_ONLY} else "MIXED"
        else:
            event_direction = "UNCERTAIN"
        confidence = max((event.confidence for _, event, _, _ in matched), default=0)
        freshness = max((event.freshness_score for _, event, _, _ in matched), default=0)
        primary = matched[0][1] if matched else None
        probability_adjustment = round(max(-15, min(8, bonus * .35 - total_penalty * .25)), 2)
        assessment = EventRiskAssessment(
            symbol=symbol, company_type=company_type, sector=sector,
            event_risk_score=round(event_score, 2), event_risk_level=level,
            event_direction=event_direction, event_confidence=round(confidence * 100, 2),
            event_freshness=round(freshness, 2), positive_event_score=round(bonus, 2),
            negative_event_score=round(negative_penalty, 2), volatility_event_score=round(volatility_score, 2),
            gap_risk_score=round(gap_score, 2), base_readiness=round(base_readiness, 2),
            adjusted_readiness=round(adjusted, 2), readiness_penalty=round(total_penalty, 2),
            readiness_bonus=round(bonus, 2), position_size_multiplier=multiplier,
            effective_risk_multiplier=multiplier, probability_adjustment=probability_adjustment,
            hard_block=hard_block,
            block_reason="Scheduled or confirmed extreme event blocks new swing entries." if hard_block else None,
            overnight_hold_allowed=overnight,
            overnight_risk_reason=None if overnight else "Elevated event-driven gap risk.",
            strategy_restrictions=list(dict.fromkeys(restrictions)),
            matched_events=[event.to_dict() | {"candidate_event_score": round(score, 2),
                                               "candidate_direction": direction.value,
                                               "decay_factor": decay_factor}
                            for score, event, direction, decay_factor in matched],
            reasons=[reason for _, event, _, _ in matched for reason in event.reasons], warnings=warnings,
            data_state=data_state, primary_category=primary.category.value if primary else "NONE",
            impact_duration=primary.expected_duration.value if primary else "INTRADAY",
            decay_model=primary.decay_model if primary else "EXPONENTIAL",
            current_decay_factor=matched[0][3] if matched else 1.0,
            directional_bonus=round(bonus, 2), volatility_penalty=round(volatility_penalty, 2),
            gap_risk_penalty=round(gap_penalty, 2), uncertainty_penalty=round(uncertainty_penalty, 2),
            manual_override_applied=any(event.source_type == EventSourceType.MANUAL_OVERRIDE
                                        for _, event, _, _ in matched),
        )
        logger.info("%s event risk: score=%.2f level=%s direction=%s readiness=%.1f->%.1f size=%.2f",
                    symbol, event_score, level, event_direction, base_readiness, adjusted, multiplier)
        context.timings["event_candidate_scoring_seconds"] = round(
            float(context.timings.get("event_candidate_scoring_seconds", 0)) + perf_counter() - started, 3)
        return assessment
