from dataclasses import dataclass, field


@dataclass(slots=True)
class HistoricalProfile:
    symbol: str

    years_analyzed: int = 10

    average_monthly_return: float = 0.0
    average_weekly_return: float = 0.0

    annualized_return: float = 0.0

    annualized_volatility: float = 0.0

    max_drawdown: float = 0.0

    win_rate: float = 0.0

    positive_months: int = 0
    negative_months: int = 0

    average_gap_up: float = 0.0
    average_gap_down: float = 0.0

    seasonality_score: float = 0.0

    consistency_score: float = 0.0

    liquidity_score: float = 0.0

    premium_score: float = 0.0

    historical_score: float = 0.0

    metadata: dict = field(default_factory=dict)