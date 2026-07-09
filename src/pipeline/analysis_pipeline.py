"""
Analysis Pipeline

Coordinates all analysis engines.
"""

from src.market.market_regime import MarketRegime
from src.market_data.market_data_hub import MarketDataHub
from src.models.analysis_result import AnalysisResult
from src.technical.technical_engine import TechnicalEngine


class AnalysisPipeline:

    def __init__(self):

        self.market_data = MarketDataHub()
        self.technical_engine = TechnicalEngine()

    def analyze(self, symbol: str):

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

        # Future integrations
        # result.candlestick = ...
        # result.breakout = ...
        # result.relative_strength = ...
        # result.trade_plan = ...
        # result.position_size = ...
        # result.sector = ...
        # result.news = ...

        return result