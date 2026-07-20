from __future__ import annotations

from datetime import date

from src.options.models.option_chain import OptionChain


class ShortPutStrikeSelector:
    @staticmethod
    def strike_band(spot: float, minimum_otm_percent: float, maximum_otm_percent: float) -> tuple[float, float]:
        return (
            spot * (1 - maximum_otm_percent / 100),
            spot * (1 - minimum_otm_percent / 100),
        )

    @classmethod
    def ranked_candidates(cls, chains: list[OptionChain], spot: float, settings,
                          support: float | None = None, atr: float | None = None):
        today = date.today()
        valid_chains = []
        for chain in chains:
            dte = (date.fromisoformat(chain.expiry) - today).days
            if settings.short_put_min_dte <= dte <= settings.short_put_max_dte:
                valid_chains.append((chain, dte))
        if not valid_chains:
            return [], None, "NO_VALID_EXPIRY"
        monthly_expiries = {}
        for chain, _ in valid_chains:
            expiry = date.fromisoformat(chain.expiry)
            key = (expiry.year, expiry.month)
            monthly_expiries[key] = max(monthly_expiries.get(key, expiry), expiry)

        lower, upper = cls.strike_band(
            spot, settings.short_put_min_otm_percent, settings.short_put_max_otm_percent
        )
        # A narrow percentage band can fall between exchange strike intervals
        # and misleadingly result in a one-contract "scan".  The band remains
        # the target, but an under-populated band is supplemented with the two
        # nearest listed strikes on either side so premium/delta trade-offs are
        # actually evaluated before rejection.
        eligible_by_expiry = {}
        for chain, _ in valid_chains:
            in_band = [put for put in chain.puts if lower <= put.strike <= upper]
            if len(in_band) < 2:
                below = sorted((put for put in chain.puts if put.strike < lower),
                               key=lambda put: put.strike, reverse=True)[:2]
                above = sorted((put for put in chain.puts if upper < put.strike < spot),
                               key=lambda put: put.strike)[:2]
                in_band = [*below, *in_band, *above]
            eligible_by_expiry[chain.expiry] = {put.symbol for put in in_band}
        ranked = []
        for chain, dte in valid_chains:
            for put in chain.puts:
                if put.symbol in eligible_by_expiry[chain.expiry]:
                    target_delta = (
                        settings.short_put_target_delta_min
                        + settings.short_put_target_delta_max
                    ) / 2
                    delta_penalty = abs(abs(put.delta) - target_delta) if put.delta is not None else 1
                    midpoint = (put.bid + put.ask) / 2 if put.bid > 0 and put.ask > 0 else 0
                    spread = (put.ask - put.bid) / midpoint * 100 if midpoint > 0 else float("inf")
                    violations = sum((
                        put.bid <= 0 or put.ask <= 0 or put.ask < put.bid,
                        put.open_interest < settings.short_put_min_open_interest,
                        put.volume < settings.short_put_min_volume,
                        spread > settings.short_put_max_bid_ask_spread_percent,
                        put.bid < settings.short_put_min_premium,
                        bool(settings.short_put_require_strike_below_support and support is not None and put.strike >= support),
                        bool(atr and (spot - put.strike) / atr < settings.short_put_min_atr_coverage),
                        bool(put.delta is not None and not settings.short_put_target_delta_min <= abs(put.delta) <= settings.short_put_target_delta_max),
                        bool(put.delta is not None and (1 - abs(put.delta)) * 100 < settings.short_put_min_probability_otm),
                    ))
                    expiry_date = date.fromisoformat(chain.expiry)
                    monthly_penalty = expiry_date != monthly_expiries[(expiry_date.year, expiry_date.month)]
                    probability_penalty = abs(put.delta) if put.delta is not None else 1
                    # Once hard eligibility failures are minimized, prefer the
                    # contract closest to the configured delta target with a
                    # useful executable credit and strong liquidity. Premium
                    # is deliberately capped so a rich but risky near-ATM Put
                    # cannot overwhelm delta/probability discipline.
                    premium_quality = min(
                        put.bid / max(settings.short_put_min_premium, .01), 3.0
                    )
                    ranked.append((violations, monthly_penalty, delta_penalty, probability_penalty,
                                   spread, -put.open_interest, -put.volume, -premium_quality,
                                   chain, dte, put))
        if not ranked:
            return [], (lower, upper), "NO_STRIKE_IN_OTM_BAND"
        return sorted(ranked, key=lambda row: row[:8]), (lower, upper), None

    @classmethod
    def select(cls, chains: list[OptionChain], spot: float, settings,
               support: float | None = None, atr: float | None = None):
        ranked, band, error = cls.ranked_candidates(chains, spot, settings, support, atr)
        if error:
            return None, band, error
        *_, chain, dte, put = ranked[0]
        return (chain, dte, put), band, None
