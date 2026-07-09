from src.data_collection.downloader import StockDownloader
from src.indicators.pipeline import IndicatorPipeline
from src.trade_setup.entry_analyzer import EntryAnalyzer


def main():

    symbol = "RELIANCE.NS"

    downloader = StockDownloader()

    df = downloader.download(symbol)

    df = IndicatorPipeline.run(df)

    result = EntryAnalyzer.analyze(df)

    print("\n")
    print("=" * 70)
    print("ENTRY ANALYSIS")
    print("=" * 70)

    for key, value in result.items():

        print(f"{key:22}: {value}")

    print("=" * 70)


if __name__ == "__main__":

    main()