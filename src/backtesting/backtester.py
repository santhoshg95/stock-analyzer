"""
Simple Backtesting Engine (Version 1)
"""

from src.backtesting.trade import Trade


class Backtester:

    @staticmethod
    def run(df):

        trades = []

        # --------------------------------------------------
        # Very Simple Demo Strategy
        #
        # Buy when EMA20 > EMA50
        # Exit when EMA20 < EMA50
        # --------------------------------------------------

        in_trade = False

        entry_price = 0

        quantity = 100

        for i in range(50, len(df)):

            row = df.iloc[i]

            close = float(row["Close"])

            ema20 = float(row["EMA20"])

            ema50 = float(row["EMA50"])

            if not in_trade:

                if ema20 > ema50:

                    in_trade = True

                    entry_price = close

            else:

                if ema20 < ema50:

                    exit_price = close

                    pnl = (exit_price - entry_price) * quantity

                    trades.append(

                        Trade(

                            entry_price=entry_price,

                            exit_price=exit_price,

                            quantity=quantity,

                            pnl=round(pnl, 2),

                            result="WIN" if pnl > 0 else "LOSS"

                        )

                    )

                    in_trade = False

        return trades