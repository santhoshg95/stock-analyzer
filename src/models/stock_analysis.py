"""
Stock Analysis Data Model
"""

from dataclasses import asdict, dataclass


@dataclass
class StockAnalysis:
    """
    Represents the complete analysis of a stock.
    """

    # --------------------------------------------------
    # Basic Information
    # --------------------------------------------------

    symbol: str
    current_price: float

    # --------------------------------------------------
    # Trend
    # --------------------------------------------------

    ema20: float
    ema50: float
    ema200: float
    trend: str

    # --------------------------------------------------
    # RSI
    # --------------------------------------------------

    rsi: float
    rsi_signal: str

    # --------------------------------------------------
    # MACD
    # --------------------------------------------------

    macd: float
    macd_signal_line: float
    macd_histogram: float
    macd_signal: str

    # --------------------------------------------------
    # ATR
    # --------------------------------------------------

    atr: float
    expected_low: float
    expected_high: float

    # --------------------------------------------------
    # Volume
    # --------------------------------------------------

    volume: int
    average_volume: float
    relative_volume: float
    volume_signal: str

    # --------------------------------------------------
    # Score
    # --------------------------------------------------

    score: int
    max_score: int
    recommendation: str

    # --------------------------------------------------
    # Utility Methods
    # --------------------------------------------------

    def to_dict(self):
        """
        Convert the dataclass into a dictionary.
        """
        return asdict(self)

    def __str__(self):
        return (
            f"{self.symbol} | "
            f"Score: {self.score}/{self.max_score} | "
            f"Trend: {self.trend} | "
            f"Recommendation: {self.recommendation}"
        )

    def __repr__(self):
        return self.__str__()