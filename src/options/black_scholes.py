"""Black-Scholes implied-volatility and Greek calculations for options."""

from __future__ import annotations

from math import erf, exp, log, pi, sqrt


def _normal_cdf(value: float) -> float:
    return (1 + erf(value / sqrt(2))) / 2


def _normal_pdf(value: float) -> float:
    return exp(-(value * value) / 2) / sqrt(2 * pi)


def price_and_greeks(spot: float, strike: float, years: float, rate: float, volatility: float, option_type: str):
    if min(spot, strike, years, volatility) <= 0:
        return None
    root_time = sqrt(years)
    d1 = (log(spot / strike) + (rate + volatility * volatility / 2) * years) / (volatility * root_time)
    d2 = d1 - volatility * root_time
    discount = exp(-rate * years)
    gamma = _normal_pdf(d1) / (spot * volatility * root_time)
    vega = spot * _normal_pdf(d1) * root_time / 100
    if option_type == "CE":
        price = spot * _normal_cdf(d1) - strike * discount * _normal_cdf(d2)
        delta = _normal_cdf(d1)
        theta = (-(spot * _normal_pdf(d1) * volatility) / (2 * root_time) - rate * strike * discount * _normal_cdf(d2)) / 365
        rho = strike * years * discount * _normal_cdf(d2) / 100
    else:
        price = strike * discount * _normal_cdf(-d2) - spot * _normal_cdf(-d1)
        delta = _normal_cdf(d1) - 1
        theta = (-(spot * _normal_pdf(d1) * volatility) / (2 * root_time) + rate * strike * discount * _normal_cdf(-d2)) / 365
        rho = -strike * years * discount * _normal_cdf(-d2) / 100
    return {"price": price, "delta": delta, "gamma": gamma, "theta": theta, "vega": vega, "rho": rho}


def implied_volatility(market_price: float, spot: float, strike: float, years: float, rate: float, option_type: str) -> float:
    if min(market_price, spot, strike, years) <= 0:
        return 0.0
    low, high = 0.01, 5.0
    for _ in range(80):
        volatility = (low + high) / 2
        result = price_and_greeks(spot, strike, years, rate, volatility, option_type)
        if result is None:
            return 0.0
        if result["price"] > market_price:
            high = volatility
        else:
            low = volatility
    return round(((low + high) / 2) * 100, 2)
