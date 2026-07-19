"""
Option Chain Model
"""

from dataclasses import dataclass, field

from src.options.models.option_contract import OptionContract


@dataclass
class OptionChain:

    symbol: str

    spot_price: float

    expiry: str

    calls: list[OptionContract] = field(default_factory=list)

    puts: list[OptionContract] = field(default_factory=list)