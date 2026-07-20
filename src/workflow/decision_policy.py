"""Final recommendation policy shared by the daily workflow and tests."""

from __future__ import annotations


def normalize_market_regime(regime: str, confidence: float) -> str:
    regime = (regime or "UNAVAILABLE").upper()
    if confidence < 50:
        if "BEARISH" in regime:
            return "UNCERTAIN_BEARISH"
        if "BULLISH" in regime:
            return "UNCERTAIN_BULLISH"
        return "UNCERTAIN"
    if confidence < 65 and regime == "STRONG_BEARISH":
        return "BEARISH"
    if confidence < 65 and regime == "STRONG_BULLISH":
        return "BULLISH"
    return regime


def market_alignment(regime: str, confidence: float, direction: str) -> dict:
    if confidence < 50 or regime.startswith("UNCERTAIN") or regime == "UNAVAILABLE":
        return {"status": "UNCERTAIN", "score": 50, "penalty": 0}
    bullish = regime in {"BULLISH", "STRONG_BULLISH"}
    bearish = regime in {"BEARISH", "STRONG_BEARISH"}
    if not bullish and not bearish:
        return {"status": "NEUTRAL", "score": 50, "penalty": 0}
    aligned = (bullish and direction == "BULLISH") or (bearish and direction == "BEARISH")
    return ({"status": "ALIGNED", "score": 85, "penalty": 0} if aligned
            else {"status": "CONFLICT", "score": 25, "penalty": 12})


def pcr_adjustment(pcr: float | None, direction: str) -> float:
    if pcr is None:
        return 0
    if direction == "BULLISH":
        return 6 if pcr >= 1 else 2 if pcr >= .8 else -3 if pcr >= .6 else -7
    if direction == "BEARISH":
        return 6 if pcr <= .7 else 2 if pcr <= .9 else -3 if pcr <= 1.2 else -7
    return 0


def option_confidence_status(confidence: float | None) -> str:
    if confidence is None:
        return "UNAVAILABLE"
    return ("CONFIRMED" if confidence >= 70 else "NEUTRAL" if confidence >= 50
            else "CONFLICT" if confidence >= 35 else "UNRELIABLE")


def market_risk_scale(confidence: float, available: bool = True) -> float:
    if not available:
        return 1.0
    if confidence < 50:
        return .5
    if confidence < 65:
        return .75
    return 1.0


def combine_strategy_eligibility(entry_confirmed: bool, equity_risk_reward: float,
                                 minimum_equity_risk_reward: float,
                                 short_put_approved: bool) -> dict:
    """Keep equity and short-Put decisions independent, then combine them."""
    equity_approved = entry_confirmed and equity_risk_reward >= minimum_equity_risk_reward
    return {
        "equity_approved": equity_approved,
        "short_put_approved": short_put_approved,
        "any_approved": equity_approved or short_put_approved,
    }


def classify_setup(trend: str, momentum: str) -> str:
    trend, momentum = (trend or "").upper(), (momentum or "").upper()
    if "BULLISH" in trend and "BEARISH" in momentum:
        return "BULLISH_PULLBACK"
    if "BEARISH" in trend and "BULLISH" in momentum:
        return "BEARISH_BOUNCE"
    if "BULLISH" in trend and "BULLISH" in momentum:
        return "BULLISH_CONTINUATION"
    if "BEARISH" in trend and "BEARISH" in momentum:
        return "BEARISH_CONTINUATION"
    return "MIXED"
