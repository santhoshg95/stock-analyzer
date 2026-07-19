"""
Analysis Pipeline

Coordinates all analysis engines.
"""

from typing import Optional

from src.market.market_regime import MarketRegime
from src.market_data.market_data_hub import MarketDataHub
from src.models.analysis_result import AnalysisResult
from src.technical.technical_engine import TechnicalEngine


class AnalysisPipeline:

    def __init__(
        self,
        market_data: Optional[MarketDataHub] = None,
        technical_engine: Optional[TechnicalEngine] = None,
    ):

        self.market_data = market_data or MarketDataHub()
        self.technical_engine = technical_engine or TechnicalEngine()

        # Optional engines
        self.breakout_engine = None
        self.candlestick_engine = None
        self.relative_strength_engine = None
        self.sector_engine = None
        self.news_engine = None
        self.trade_plan_engine = None
        self.position_size_engine = None

    # ---------------------------------------------------------

    def register_breakout_engine(self, engine):

        self.breakout_engine = engine

    def register_candlestick_engine(self, engine):

        self.candlestick_engine = engine

    def register_relative_strength_engine(self, engine):

        self.relative_strength_engine = engine

    def register_sector_engine(self, engine):

        self.sector_engine = engine

    def register_news_engine(self, engine):

        self.news_engine = engine

    def register_trade_plan_engine(self, engine):

        self.trade_plan_engine = engine

    def register_position_size_engine(self, engine):

        self.position_size_engine = engine

    # ---------------------------------------------------------

    def analyze(self, symbol: str) -> AnalysisResult:

        result = AnalysisResult(symbol=symbol)

        # ---------------------------------------------------
        # Market Analysis
        # ---------------------------------------------------

        snapshot = self.market_data.get_market_snapshot()

        result.market = MarketRegime.classify(snapshot)

        # ---------------------------------------------------
        # Technical Analysis
        # ---------------------------------------------------

        result.technical = self.technical_engine.analyze(symbol)

        # ---------------------------------------------------
        # Optional Integrations
        # ---------------------------------------------------

        if self.breakout_engine:

            result.breakout = self.breakout_engine.analyze(symbol)

        if self.candlestick_engine:

            result.candlestick = self.candlestick_engine.analyze(symbol)

        if self.relative_strength_engine:

            result.relative_strength = self.relative_strength_engine.analyze(symbol)

        if self.sector_engine:

            result.sector = self.sector_engine.analyze(symbol)

        if self.news_engine:

            result.news = self.news_engine.analyze(symbol)

        if self.trade_plan_engine:

            result.trade_plan = self.trade_plan_engine.generate(result)

        if self.position_size_engine:

            result.position_size = self.position_size_engine.calculate(result)

        return result