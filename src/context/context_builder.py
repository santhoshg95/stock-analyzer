"""
Context Builder

Builds a complete StockContext object used by every AI engine.

Version 3
"""

from pathlib import Path

from src.context.stock_context import StockContext
from src.historical import HistoricalEngine


class ContextBuilder:

    def __init__(self):

        self.history_directory = Path("data/history")

        self.history_directory.mkdir(parents=True, exist_ok=True)

        self.historical_engine = HistoricalEngine(
            data_directory=self.history_directory
        )

    def build(self, symbol: str) -> StockContext:

        context = StockContext(symbol=symbol)

        self._initialize_basic(context)

        self._initialize_analysis(context)

        self._initialize_historical(context)

        self._initialize_qualification(context)

        self._initialize_ai(context)

        self._initialize_scores(context)

        self._load_historical(context)

        return context

    # ---------------------------------------------------
    # Initializers
    # ---------------------------------------------------

    def _initialize_basic(self, context: StockContext):

        context.metadata = {
            "symbol": context.symbol
        }

    def _initialize_analysis(self, context: StockContext):

        context.analysis = None
        context.market = None
        context.sector = None
        context.technical = None
        context.news = None
        context.options = None

    def _initialize_historical(self, context: StockContext):

        context.stock_dna = None

        context.historical_profile = None

        context.monthly_score = 0.0

        context.historical_score = 0.0

        context.seasonality_score = 0.0

    def _initialize_qualification(self, context: StockContext):

        context.qualified = True

        context.qualification_reason = ""

    def _initialize_ai(self, context: StockContext):

        context.evidence = None

        context.factors = None

        context.decision = None

        context.strategy = None

        context.trade = None

    def _initialize_scores(self, context: StockContext):

        context.technical_score = 0.0

        context.option_score = 0.0

        context.market_score = 0.0

        context.news_score = 0.0

        context.strategy_score = 0.0

        context.risk_score = 0.0

        context.opportunity_score = 0.0

        context.confidence = 0.0

        context.rank = 0

        context.recommendation = ""

    # ---------------------------------------------------
    # Historical Intelligence
    # ---------------------------------------------------

    def _load_historical(self, context: StockContext):

        try:

            profile, dna = self.historical_engine.analyze(
                context.symbol
            )

            context.historical_profile = profile

            context.stock_dna = dna

            context.historical_score = profile.historical_score

            context.monthly_score = profile.consistency_score

            context.seasonality_score = profile.seasonality_score

        except Exception as ex:

            print(f"[HistoricalEngine] {context.symbol}: {ex}")

        return context