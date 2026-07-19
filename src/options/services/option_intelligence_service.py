"""
Option Intelligence Service

Responsible for enriching the StockContext with option intelligence.
"""

from src.context.stock_context import StockContext

from src.options.engine.option_engine import OptionEngine
from src.options.models.option_context import OptionContext


class OptionIntelligenceService:
    """
    Runs the complete option intelligence pipeline.

    Responsibilities:
        - Execute OptionEngine
        - Build OptionContext
        - Attach it to StockContext
    """

    def __init__(self):

        self.engine = OptionEngine()

    def enrich(self, context: StockContext) -> StockContext:
        """
        Enrich StockContext with option intelligence.

        Parameters
        ----------
        context : StockContext

        Returns
        -------
        StockContext
        """

        if context.options is None:
            context.options = OptionContext()

        if context.options.chain is None:
            return context

        analysis = self.engine.analyze(
            context.options.chain
        )

        context.options.analysis = analysis

        return context