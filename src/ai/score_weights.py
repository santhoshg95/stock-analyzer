"""
AI Score Weights

All engine weights are centralized here.
"""


class ScoreWeights:

    MARKET = 15

    SECTOR = 15

    TECHNICAL = 25

    CANDLESTICK = 10

    BREAKOUT = 10

    RELATIVE_STRENGTH = 10

    NEWS = 5

    OPTION = 10

    TOTAL = (
        MARKET
        + SECTOR
        + TECHNICAL
        + CANDLESTICK
        + BREAKOUT
        + RELATIVE_STRENGTH
        + NEWS
        + OPTION
    )