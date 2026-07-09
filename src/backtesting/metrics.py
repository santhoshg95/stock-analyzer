"""
Backtest Metrics
"""


class Metrics:

    @staticmethod
    def summarize(trades):

        total = len(trades)

        wins = sum(1 for t in trades if t.pnl > 0)

        losses = total - wins

        total_pnl = sum(t.pnl for t in trades)

        win_rate = 0

        if total > 0:

            win_rate = wins / total * 100

        return {

            "total_trades": total,

            "wins": wins,

            "losses": losses,

            "win_rate": round(win_rate, 2),

            "total_pnl": round(total_pnl, 2)

        }