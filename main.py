import argparse
import json

from src.application.errors import PlatformError
from src.application.platform import TradingPlatform


def main():
    parser = argparse.ArgumentParser(description="AI Quantitative Trading Platform")
    subcommands = parser.add_subparsers(dest="command", required=True)
    for name in ("analyze", "backtest"):
        command = subcommands.add_parser(name)
        command.add_argument("symbol")
    suggest = subcommands.add_parser("suggest", help="rank the available cached stocks")
    suggest.add_argument("--limit", type=int, default=5)
    suggest.add_argument("--minimum-score", type=int, default=40)
    paper = subcommands.add_parser("papertrade")
    paper.add_argument("symbol")
    paper.add_argument("side", choices=("BUY", "SELL"))
    paper.add_argument("--quantity", type=int)
    subcommands.add_parser("portfolio")
    args = parser.parse_args()
    platform = TradingPlatform()
    try:
        if args.command == "analyze":
            result = platform.analyze(args.symbol)
        elif args.command == "backtest":
            result = platform.backtest(args.symbol)
        elif args.command == "suggest":
            result = platform.suggest_stocks(args.limit, args.minimum_score)
        elif args.command == "papertrade":
            result = platform.paper_trade(args.symbol, args.side, args.quantity)
        else:
            result = platform.portfolio()
    except PlatformError as exc:
        parser.error(str(exc))
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":

    main()
