import unittest

from src.options.black_scholes import implied_volatility, price_and_greeks


class OptionPricingTests(unittest.TestCase):
    def test_implied_volatility_reprices_market_premium(self):
        original = price_and_greeks(100, 100, 30 / 365, .07, .25, "CE")
        iv = implied_volatility(original["price"], 100, 100, 30 / 365, .07, "CE")
        calculated = price_and_greeks(100, 100, 30 / 365, .07, iv / 100, "CE")
        self.assertAlmostEqual(iv, 25, delta=.1)
        self.assertAlmostEqual(calculated["price"], original["price"], places=2)
        self.assertGreater(calculated["delta"], 0)
