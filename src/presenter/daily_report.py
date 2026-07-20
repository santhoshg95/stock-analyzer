"""Human-readable CLI presentation for the final daily trade report."""

from __future__ import annotations

from typing import Any


class DailyReportPresenter:
    """Render a report returned by ``TradingPlatform.daily_report``."""

    @staticmethod
    def _money(value: Any) -> str:
        return "N/A" if value is None else f"₹{float(value):,.2f}"

    @classmethod
    def render(cls, report: dict[str, Any]) -> str:
        line = "=" * 68
        market, summary = report["market"], report["summary"]
        rows = [line, "                    AI TRADING ASSISTANT", line,
                f"DATE                 : {report['date']}",
                f"MARKET               : {market['regime']}",
                f"MARKET CONFIDENCE    : {market['confidence']}%", line]
        for trade in report["trades"]:
            levels, risk = trade["levels"], trade["risk"]
            rows.extend([
                f"TOP TRADE #{trade['rank']} — {trade['symbol']}", "-" * 68,
                f"Sector               : {trade['sector']}",
                f"Current price        : {cls._money(trade['current_price'])}",
                f"AI score             : {trade['ai_score']}/100",
                f"News sentiment       : {trade['news']['sentiment']} ({trade['news']['score']:+.1f})",
                f"Confidence           : {trade['confidence']}%",
                f"Estimated probability: {trade['probability']}%",
                f"Strategy             : {trade['strategy']} ({trade['time_frame']})",
                f"Trend / momentum     : {trade['technical']['trend']} / {trade['technical']['momentum']}",
                f"Stock liquidity      : {trade['stock_liquidity']['status']} ({trade['stock_liquidity']['average_daily_turnover_crore']} cr avg/day)",
                f"F&O trust filter      : {trade['trust']['status']} ({trade['trust']['score']}/100)",
                f"Sector / relative str: {trade['sector_context']['rating']} / {trade['relative_strength']['rating']}",
                f"Support / resistance : {cls._money(levels['support'])} / {cls._money(levels['resistance'])}",
                f"Entry / stop         : {cls._money(levels['entry'])} / {cls._money(levels['stop_loss'])}",
                f"Targets              : {cls._money(levels['target_1'])}, {cls._money(levels['target_2'])}, {cls._money(levels['target_3'])}",
                f"Risk reward          : 1:{levels['risk_reward']}",
                f"Position size        : {risk['quantity']} shares (max risk {cls._money(risk['risk_amount'])})",
            ])
            option = trade["option_strategy"]
            if option.get("available"):
                plan = option.get("trade", {})
                rows.append(f"Option strategy      : {plan.get('strategy', option.get('strategy', 'N/A'))}")
                rows.append(f"PCR / Max pain       : {option.get('pcr', 'N/A')} / {option.get('max_pain', 'N/A')}")
                rows.append(f"IV / option confidence: {option.get('iv_rank', 'N/A')} / {option.get('confidence', 'N/A')}%")
                rows.append(f"Option hedge target  : {cls._money(plan.get('hedge_strike_target'))} (technical level)")
                for leg in plan.get("legs", []):
                    rows.append(f"  {leg['side']} {leg['quantity']} × {leg['strike']} {leg['option_type']} @ {cls._money(leg['premium'])}")
                rows.append(f"Option max loss      : {cls._money(plan.get('maximum_loss'))}")
            else:
                rows.append("Option strategy      : unavailable (requires live Kite option data)")
            rows.append("Reasons              : " + "; ".join(trade["ai_reasoning"][:3]))
            if trade["validation"]["conflicts"]:
                rows.append("Conflicts            : " + "; ".join(trade["validation"]["conflicts"]))
            for headline in trade["news"].get("headlines", [])[:2]:
                rows.append(f"News                 : {headline['title']}")
            rows.append(line)
        rows.extend([
            "TODAY'S MARKET SUMMARY", "-" * 68,
            f"Stocks scanned       : {summary['stocks_scanned']}",
            f"Stocks shortlisted   : {summary['stocks_shortlisted']}",
            f"Conflicts rejected   : {summary.get('conflicts_rejected', 0)}",
            f"Trades generated     : {summary['trades_generated']}",
            f"Best sector          : {summary['best_sector']}",
            f"Best option strategy : {summary['best_option_strategy']}",
            f"Average probability  : {summary['average_probability']}%",
            f"Market risk          : {summary['market_risk']}",
            f"Recommendation       : {summary['recommendation']}", line,
            *(
                ["REJECTED CANDIDATES", "-" * 68]
                + [f"{item['symbol']}: {'; '.join(item['reasons'])}" for item in report.get("rejected", [])[:10]]
                + [line]
                if report.get("rejected") else []
            ),
            "Research and paper-trading use only; no order has been placed.",
        ])
        return "\n".join(rows)
