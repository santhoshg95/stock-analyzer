"""
Application Entry Point
"""

from src.analysis.analyzer import StockAnalyzer
from src.data_collection.downloader import StockDownloader
from src.indicators.pipeline import IndicatorPipeline


def main():

    downloader = StockDownloader()

    df = downloader.download_stock("RELIANCE")

    if df is None:
        return

    # Apply all indicators
    df = IndicatorPipeline.run(df)

    # Analyze the latest values
    StockAnalyzer.analyze("RELIANCE", df)


if __name__ == "__main__":
    main()