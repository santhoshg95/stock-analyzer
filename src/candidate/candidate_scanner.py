"""
Candidate Scanner

Scans F&O stocks in parallel.
"""

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from src.ai.ai_score_engine import AIScoreEngine
from src.models.candidate_result import CandidateResult
from src.pipeline.analysis_pipeline import AnalysisPipeline


class CandidateScanner:

    def __init__(self, workers=10):

        self.pipeline = AnalysisPipeline()

        self.score_engine = AIScoreEngine()

        self.workers = workers

    # ----------------------------------------------------

    def analyze_stock(self, symbol):

        try:

            report = self.pipeline.analyze(symbol)

            score = self.score_engine.calculate(report)

            return CandidateResult(

                symbol=symbol,

                score=score.total,

                percentage=score.percentage,

                market=report.market.status,

                technical=report.technical.status

            )

        except Exception as ex:

            print(f"{symbol} -> {ex}")

            return None

    # ----------------------------------------------------

    def scan(self, symbols):

        results = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:

            futures = {

                executor.submit(

                    self.analyze_stock,

                    symbol

                ): symbol

                for symbol in symbols

            }

            for future in as_completed(futures):

                result = future.result()

                if result:

                    results.append(result)

        return results