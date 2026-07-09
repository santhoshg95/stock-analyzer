"""
AI Trading Assistant

Main Entry Point
"""

from pathlib import Path

from src.report.report_generator import ReportGenerator
from src.screener.scanner import StockScanner


def main():

    # ---------------------------------------------------------
    # Stock Universe
    # ---------------------------------------------------------

    symbols = [

        "RELIANCE",
        "TCS",
        "INFY",
        "HDFCBANK",
        "ICICIBANK",
        "SBIN",
        "LT",
        "AXISBANK",
        "MARUTI",
        "BAJFINANCE"

    ]

    # ---------------------------------------------------------
    # Scan Stocks
    # ---------------------------------------------------------

    scanner = StockScanner()

    analyses = scanner.scan(symbols)

    # ---------------------------------------------------------
    # Generate Report
    # ---------------------------------------------------------

    report = ReportGenerator.create_dataframe(analyses)

    if report.empty:

        print("No stocks scanned.")

        return

    # ---------------------------------------------------------
    # Display Report
    # ---------------------------------------------------------

    print()

    print("=" * 100)
    print("TOP STOCKS")
    print("=" * 100)

    display_columns = [

        "symbol",
        "score",
        "trend",
        "rsi",
        "relative_volume",
        "recommendation"

    ]

    print(report[display_columns])

    # ---------------------------------------------------------
    # Save Report
    # ---------------------------------------------------------

    reports_dir = Path("reports")

    reports_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    report_file = reports_dir / "screener.csv"

    report.to_csv(
        report_file,
        index=False
    )

    print()

    print("=" * 100)
    print("REPORT GENERATED SUCCESSFULLY")
    print("=" * 100)

    print(f"Location : {report_file.resolve()}")

    print("=" * 100)


if __name__ == "__main__":
    main()