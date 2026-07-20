import unittest

from src.options.entry_validator import OptionEntryValidator
from src.options.models.option_chain import OptionChain
from src.options.models.option_contract import OptionContract


def contract(strike, oi, change, delta=.5, theta=-.2, premium=10):
    return OptionContract("TEST", "2026-07-30", strike, "CE", premium, premium - .1, premium + .1,
                          20_000, oi, change, 25, delta=delta, theta=theta, lot_size=100)


class OptionEntryValidatorTests(unittest.TestCase):
    def test_blocks_bullish_entry_below_high_call_oi_resistance(self):
        chain = OptionChain("TEST", 99, "2026-07-30", calls=[contract(100, 1_000_000, 5000)])
        trade = {"legs": [{"side": "BUY", "delta": .5, "theta": -.2, "premium": 10,
                            "implied_volatility": 25}]}
        result = OptionEntryValidator.validate(chain, trade, "BULLISH")
        self.assertFalse(result["approved"])
        self.assertIn("high Call-OI resistance", result["reasons"][0])
