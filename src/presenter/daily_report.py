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
        for trade in [*report["trades"], *report.get("watchlist", [])]:
            levels, risk = trade["levels"], trade["risk"]
            rows.extend([
                f"{trade['status']} #{trade['rank']} — {trade['symbol']}", "-" * 68,
                f"Setup / action       : {trade['setup']} / {trade['action']}",
                f"Market alignment     : {trade['market_alignment']['status']}",
                f"Sector               : {trade['sector']}",
                f"Current price        : {cls._money(trade['current_price'])}",
                f"AI score             : {trade['ai_score']}/100",
                f"News sentiment       : {trade['news']['sentiment']} ({trade['news']['score']:+.1f})",
                f"Model confidence     : {trade['model_confidence']['decision_confidence']}%",
                f"Estimated probability: {trade['model_confidence']['estimated_probability']}%",
                f"Trade eligibility    : {trade['trade_eligibility']['status']}",
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
                f"Risk scaling         : {trade['risk_policy']['position_scale'] * 100:.0f}% position; {trade['risk_policy']['effective_risk_percent']}% effective risk",
                f"Option account       : {cls._money(trade['option_budget_policy']['capital_available'])} capital; {cls._money(trade['option_budget_policy']['risk_per_trade'])} max risk/trade",
            ])
            seasonal = trade.get("current_month_seasonality", {})
            rows.append(
                f"{seasonal.get('month_name', 'Month')} history        : "
                f"avg {seasonal.get('average_return_percent', 'N/A')}%, "
                f"median {seasonal.get('median_return_percent', 'N/A')}%, "
                f"wins {seasonal.get('win_rate_percent', 'N/A')}% "
                f"({seasonal.get('sample_years', 0)} years; {seasonal.get('sample_quality', 'INSUFFICIENT')})"
            )
            rows.append(
                f"Current month MTD    : {seasonal.get('current_mtd_return_percent', 'N/A')}% "
                f"({seasonal.get('versus_history', 'UNAVAILABLE')}; score impact {seasonal.get('score_adjustment', 0):+.2f})"
            )
            regime = trade.get("regime_history", {})
            rows.append(
                f"Regime history       : {regime.get('regime', 'UNAVAILABLE')} — "
                f"{regime.get('win_rate_percent', 'N/A')}% win rate, "
                f"{regime.get('sample_count', 0)} samples ({regime.get('sample_quality', 'INSUFFICIENT')}); "
                f"score impact {regime.get('score_adjustment', 0):+.2f}"
            )
            option = trade["option_strategy"]
            if option.get("available"):
                plan = option.get("trade", {})
                rows.append(f"Option strategy      : {plan.get('strategy', option.get('strategy', 'N/A'))}")
                rows.append(f"PCR / Max pain       : {option.get('pcr', 'N/A')} / {option.get('max_pain', 'N/A')}")
                rows.append(f"IV / option confidence: {option.get('iv_rank', 'N/A')} / {option.get('confidence', 'N/A')}%")
                rows.append(f"Option hedge target  : {cls._money(plan.get('hedge_strike_target'))} (technical level)")
                validation = option.get("entry_validation", {})
                rows.append(f"Option entry check   : {'APPROVED' if validation.get('approved') else 'BLOCKED'}")
                for warning in validation.get("warnings", []):
                    rows.append(f"Option warning       : {warning}")
                for leg in plan.get("legs", []):
                    rows.append(f"  {leg['side']} {leg['quantity']} × {leg['strike']} {leg['option_type']} @ {cls._money(leg['premium'])}")
                rows.append(f"Option max loss      : {cls._money(plan.get('maximum_loss'))}")
            else:
                rejection = option.get("rejection") or {}
                rows.append(f"Option strategy      : rejected [{rejection.get('code', option.get('error_type', 'UNAVAILABLE'))}]")
                rows.append(f"Option rejection     : {rejection.get('reason', option.get('reason', 'No executable option structure'))}")
                if rejection.get("code") == "RISK_BUDGET_EXCEEDED":
                    rows.append(f"Option budget        : needs {cls._money(rejection.get('required_budget'))}; available {cls._money(rejection.get('available_budget'))}")
                if rejection.get("maximum_loss") is not None:
                    rows.append(f"Option max loss      : {cls._money(rejection.get('maximum_loss'))}")
                if rejection.get("capital_required") is not None:
                    rows.append(f"Option capital       : needs {cls._money(rejection.get('capital_required'))}; available {cls._money(rejection.get('capital_available'))}")
            if trade["status"] == "WATCHLIST":
                readiness = trade["trade_readiness"]
                rows.append(f"Trade readiness      : {readiness['percentage']}% — {readiness['classification']}")
                for check in readiness["checks"]:
                    rows.append(f"  {'✓' if check['passed'] else '✗'} {check['name']}: {check['detail']}")
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
            f"Successfully analysed: {summary.get('analysis_succeeded', 0)}",
            f"Failed analysis      : {summary.get('analysis_failed', 0)}",
            f"Technical candidates : {summary.get('technical_passed', 0)}",
            f"Liquidity-qualified  : {summary.get('liquidity_passed', 0)}",
            f"Trust-qualified      : {summary.get('trust_passed', 0)}",
            f"Context-reviewed     : {summary.get('context_reviewed', 0)}",
            f"Risk-valid           : {summary.get('risk_valid', 0)}",
            f"Market-aligned       : {summary.get('market_aligned', 0)}",
            f"Watchlist candidates : {summary.get('watchlisted', 0)}",
            f"Option-confirmed     : {summary.get('option_confirmed', 0)}",
            f"Conflicts rejected   : {summary.get('conflicts_rejected', 0)}",
            f"Trades generated     : {summary['trades_generated']}",
            f"Best sector          : {summary['best_sector']}",
            f"Best option strategy : {summary['best_option_strategy']}",
            f"Average trade probability: {summary['average_probability']}%" if summary.get("average_probability") is not None else "Average trade probability: N/A",
            f"Average watchlist probability: {summary['average_watchlist_probability']}%" if summary.get("average_watchlist_probability") is not None else "Average watchlist probability: N/A",
            f"Market risk          : {summary['market_risk']}",
            f"Recommendation       : {summary['recommendation']}", line,
            "FILTER FUNNEL", "-" * 68,
            *[f"{item['stage']:<20}: {item['input']} in / {item['passed']} passed / {item['rejected']} rejected"
              + (f" / {item['deferred']} deferred" if item.get('deferred') else "")
              for item in report.get("filter_stages", [])],
            line,
            "CONTEXT REVIEW", "-" * 68,
            *[f"{name:<20}: {values['passed']} passed / {values['failed']} failed / {values['unavailable']} unavailable"
              for name, values in report.get("context_statistics", {}).items()],
            line,
            "SECTOR RANKING", "-" * 68,
            *[f"#{item['rank']} {item['sector']}: {item['score']}/100 ({item['rating']}, {item['candidate_count']} candidates)"
              for item in report.get("sector_ranking", [])[:10]],
            line,
            "HISTORICAL LEARNING", "-" * 68,
            f"Completed outcomes   : {report.get('historical_learning', {}).get('completed_outcomes', 0)}",
            *[f"{item['symbol']}: {item['recommendations']} recommendations, {item['wins']}W/{item['losses']}L, {item['win_rate_percent']}% ({item['confidence']})"
              for item in report.get("historical_learning", {}).get("by_symbol", [])[:5]],
            *[f"{item['setup']} in {item['market_regime']}: {item['recommendations']} samples, {item['win_rate_percent']}% ({item['confidence']})"
              for item in report.get("historical_learning", {}).get("by_setup_and_regime", [])[:5]],
            line,
            *(
                ["REJECTED CANDIDATES", "-" * 68]
                + [f"{item['symbol']}: {'; '.join(item['reasons'])}" for item in report.get("rejected", [])[:10]]
                + [line]
                if report.get("rejected") else []
            ),
            "Research and paper-trading use only; no order has been placed.",
        ])
        return "\n".join(rows)
