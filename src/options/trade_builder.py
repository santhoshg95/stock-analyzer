"""Build an explicit, reviewable option trade from an analysed option chain.

The builder deliberately returns a data structure instead of submitting an
order.  It is suitable for a recommendation/reporting workflow and keeps the
platform paper-trading only.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from src.options.models.option_chain import OptionChain


class OptionTradeBuilder:
    """Select liquid strikes and calculate defined-risk option structures."""

    @staticmethod
    def _price(contract) -> float:
        if contract.bid > 0 and contract.ask > 0:
            return round((contract.bid + contract.ask) / 2, 2)
        return round(contract.last_price, 2)

    @staticmethod
    def _nearest(contracts, target: float):
        liquid = [item for item in contracts if item.last_price > 0]
        return min(liquid or contracts, key=lambda item: abs(item.strike - target)) if contracts else None

    @classmethod
    def build(cls, chain: OptionChain, strategy: str, direction: str, support: float | None = None,
              resistance: float | None = None, risk_budget: float | None = None) -> dict[str, Any]:
        """Return a complete recommendation, or an unavailable explanation."""
        bullish = direction == "BULLISH"
        contracts = chain.calls if bullish else chain.puts
        long_leg = cls._nearest(contracts, chain.spot_price)
        if long_leg is None:
            return {"available": False, "reason": "No priced option contracts are available."}

        # Prefer a vertical spread for defined risk when a second liquid strike
        # exists.  A single long option remains an explicit fallback.
        if bullish:
            hedge_candidates = [item for item in contracts if item.strike > long_leg.strike]
            # The short call caps the spread near the technical target, rather
            # than at an arbitrary percentage away from spot.
            hedge_target = resistance if resistance and resistance > long_leg.strike else long_leg.strike * 1.03
        else:
            hedge_candidates = [item for item in contracts if item.strike < long_leg.strike]
            hedge_target = support if support and support < long_leg.strike else long_leg.strike * 0.97
        short_leg = cls._nearest(hedge_candidates, hedge_target)

        long_premium = cls._price(long_leg)
        lot_size = max(1, long_leg.lot_size)
        legs = [{"side": "BUY", **asdict(long_leg), "premium": long_premium, "quantity": lot_size}]
        result_strategy = "Long Call" if bullish else "Long Put"
        net_debit = long_premium
        maximum_profit = None
        maximum_loss = long_premium

        if short_leg is not None and cls._price(short_leg) > 0:
            short_premium = cls._price(short_leg)
            legs.append({"side": "SELL", **asdict(short_leg), "premium": short_premium, "quantity": lot_size})
            net_debit = round(long_premium - short_premium, 2)
            width = abs(short_leg.strike - long_leg.strike)
            maximum_loss = max(net_debit, 0)
            maximum_profit = round(max(width - maximum_loss, 0), 2)
            result_strategy = "Bull Call Spread" if bullish else "Bear Put Spread"

        breakeven = round(long_leg.strike + net_debit, 2) if bullish else round(long_leg.strike - net_debit, 2)
        max_loss_per_lot = round(maximum_loss * lot_size, 2)
        recommended_lots = int((risk_budget or 0) // max_loss_per_lot) if max_loss_per_lot > 0 else 0
        total_quantity = recommended_lots * lot_size
        for leg in legs:
            leg["quantity"] = total_quantity
        return {
            "available": recommended_lots > 0,
            # The reported strategy must match the actual legs.  The option
            # analysis preference is retained separately when it differs.
            "strategy": result_strategy,
            "analysis_strategy": strategy,
            "expiry": chain.expiry,
            "spot_price": round(chain.spot_price, 2),
            "legs": legs,
            "net_debit": net_debit,
            "lot_size": lot_size,
            "recommended_lots": recommended_lots,
            "recommended_quantity": total_quantity,
            "risk_budget": risk_budget,
            "net_debit_per_lot": round(net_debit * lot_size, 2),
            "maximum_profit": round(maximum_profit * lot_size, 2) if maximum_profit is not None else None,
            "maximum_loss": max_loss_per_lot,
            "breakeven": breakeven,
            "risk_defined": short_leg is not None,
            "technical_support": support,
            "technical_resistance": resistance,
            "hedge_strike_target": round(hedge_target, 2),
            "reason": None if recommended_lots > 0 else "One lot exceeds the configured maximum option risk.",
        }
