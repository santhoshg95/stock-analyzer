"""
Report Generator

Converts StockAnalysis objects into a Pandas DataFrame.
"""

from typing import List

import pandas as pd

from src.models.stock_analysis import StockAnalysis


class ReportGenerator:

    @staticmethod
    def create_dataframe(
        analyses: List[StockAnalysis]
    ) -> pd.DataFrame:

        rows = []

        for analysis in analyses:

            rows.append(analysis.to_dict())

        df = pd.DataFrame(rows)

        if df.empty:
            return df

        # ------------------------------------------
        # Sort by Score
        # ------------------------------------------

        df = df.sort_values(
            by="score",
            ascending=False
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df