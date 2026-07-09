"""
Signal Pipeline

Runs all signal generators.
"""

from typing import List
import pandas as pd

from src.signals.base_signal import Signal
from src.signals.trend_signal import TrendSignal
from src.signals.momentum_signal import MomentumSignal
from src.signals.volume_signal import VolumeSignal
from src.signals.volatility_signal import VolatilitySignal
from src.signals.support_signal import SupportSignal


class SignalPipeline:

    @staticmethod
    def run(df: pd.DataFrame) -> List[Signal]:

        return [

            TrendSignal.generate(df),

            MomentumSignal.generate(df),

            VolumeSignal.generate(df),

            VolatilitySignal.generate(df),

            SupportSignal.generate(df)

        ]