"""
Trading Engine

Central orchestrator for the AI Trading Assistant.
"""

from src.analysis.analyzer import StockAnalyzer
from src.breakout.breakout_detector import BreakoutDetector
from src.data_provider.provider import DataProvider
from src.indicators.pipeline import IndicatorPipeline
from src.trade_setup.entry_analyzer import EntryAnalyzer
from src.decision.decision_engine import DecisionEngine


class TradingEngine:

    def __init__(self):

        self.provider = DataProvider()

    def analyze(self, symbol: str):

        # --------------------------------------------------
        # Load Historical Data
        # --------------------------------------------------

        df = self.provider.get_data(symbol)

        if df is None:
            return None

        # --------------------------------------------------
        # Calculate Indicators
        # --------------------------------------------------

        df = IndicatorPipeline.run(df)

        # --------------------------------------------------
        # Technical Analysis
        # --------------------------------------------------

        analysis = StockAnalyzer.analyze(symbol, df)

        # --------------------------------------------------
        # Entry Analysis
        # --------------------------------------------------

        entry = EntryAnalyzer.analyze(df)

        # --------------------------------------------------
        # Breakout Analysis
        # --------------------------------------------------

        breakout = BreakoutDetector.analyze(df)

        # --------------------------------------------------
        # Final Decision
        # --------------------------------------------------

        decision = DecisionEngine.decide(
            {
                "analysis": analysis,
                "entry": entry,
                "breakout": breakout,
            }
        )

        # --------------------------------------------------
        # Final Trading Report
        # --------------------------------------------------

        return {

            "analysis": analysis,

            "entry": entry,

            "breakout": breakout,

            "decision": decision

        }