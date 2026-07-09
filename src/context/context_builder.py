"""
Stock Context Builder

Builds a StockContext using the existing Analysis Pipeline.
"""

from src.context.stock_context import StockContext
from src.pipeline.analysis_pipeline import AnalysisPipeline


class ContextBuilder:

    def __init__(self):

        self.pipeline = AnalysisPipeline()

    def build(self, symbol: str):

        analysis = self.pipeline.analyze(symbol)

        context = StockContext(

            symbol=symbol,

            analysis=analysis,

            market=analysis.market,

            technical=analysis.technical

        )

        return context