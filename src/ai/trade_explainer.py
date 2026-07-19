"""
Trade Explainer

Master explanation engine for AI Trading Platform.

This module converts outputs from all AI engines into a human-readable
trade report explaining WHY the AI selected a trade.

Supported Engines
-----------------
✔ Historical
✔ Technical
✔ Market
✔ News
✔ Sector
✔ Ranking
✔ Rules
✔ Factors
✔ Evidence
✔ Options
✔ Strategy
✔ Decision
✔ Confidence
✔ Position Size
✔ Trade Plan

Author:
AI Research Platform
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, List, Any


# ============================================================
# MODEL
# ============================================================

@dataclass
class TradeExplanation:

    symbol: str

    summary: str

    recommendation: str

    confidence: float

    overall_score: float

    strengths: List[str]

    weaknesses: List[str]

    opportunities: List[str]

    risks: List[str]

    execution_plan: List[str]

    monitoring_points: List[str]

    ai_reasoning: List[str]

    raw_metrics: Dict[str, Any]


# ============================================================
# TRADE EXPLAINER
# ============================================================

class TradeExplainer:

    """
    Final AI Explanation Engine.

    This class receives outputs from all engines and converts them
    into a readable report.

    Every engine contributes to the final explanation.

    """

    # ---------------------------------------------------------

    def explain(

        self,

        symbol: str,

        historical: Dict[str, Any],

        technical: Dict[str, Any],

        market: Dict[str, Any],

        strategy: Dict[str, Any],

        options: Dict[str, Any],

        decision: Dict[str, Any],

        confidence: Dict[str, Any],

        portfolio: Dict[str, Any],

        **extra,

    ) -> TradeExplanation:

        strengths = []

        weaknesses = []

        opportunities = []

        risks = []

        ai_reasoning = []

        execution = []

        monitoring = []

        # =====================================================
        # HISTORICAL
        # =====================================================

        strengths.extend(

            self._historical_strengths(historical)

        )

        risks.extend(

            self._historical_risks(historical)

        )

        # =====================================================
        # TECHNICAL
        # =====================================================

        strengths.extend(

            self._technical_strengths(technical)

        )

        weaknesses.extend(

            self._technical_weaknesses(technical)

        )

        # =====================================================
        # MARKET
        # =====================================================

        strengths.extend(

            self._market_strengths(market)

        )

        risks.extend(

            self._market_risks(market)

        )

        # =====================================================
        # OPTIONS
        # =====================================================

        strengths.extend(

            self._option_strengths(options)

        )

        risks.extend(

            self._option_risks(options)

        )

        # =====================================================
        # STRATEGY
        # =====================================================

        execution.extend(

            self._execution(

                strategy,

                portfolio,

            )

        )

        monitoring.extend(

            self._monitoring(

                technical,

                options,

            )

        )

        ai_reasoning.extend(

            self._ai_reasoning(

                historical,

                technical,

                market,

                strategy,

                options,

            )

        )

        overall_score = decision.get(

            "score",

            decision.get(

                "overall_score",

                0,

            ),

        )

        summary = (

            f"{decision.get('recommendation','WATCH')} "

            f"with "

            f"{confidence.get('confidence',0):.2f}% "

            f"confidence."

        )

        return TradeExplanation(

            symbol=symbol,

            summary=summary,

            recommendation=decision.get(

                "recommendation",

                "WATCH",

            ),

            confidence=confidence.get(

                "confidence",

                0,

            ),

            overall_score=overall_score,

            strengths=strengths,

            weaknesses=weaknesses,

            opportunities=opportunities,

            risks=risks,

            execution_plan=execution,

            monitoring_points=monitoring,

            ai_reasoning=ai_reasoning,

            raw_metrics={

                "historical": historical,

                "technical": technical,

                "market": market,

                "strategy": strategy,

                "options": options,

                "decision": decision,

                "confidence": confidence,

                "portfolio": portfolio,

                **extra,

            },

        )


    # ============================================================
    # HISTORICAL STRENGTHS
    # ============================================================

    def _historical_strengths(self, historical):

        strengths = []

        if not historical:
            return strengths

        success_rate = historical.get("success_rate", 0)

        if success_rate >= 80:
            strengths.append(
                f"Historical success rate is excellent ({success_rate:.1f}%)."
            )

        elif success_rate >= 70:
            strengths.append(
                f"Historical success rate is good ({success_rate:.1f}%)."
            )

        avg_return = historical.get("average_return", 0)

        if avg_return > 5:
            strengths.append(
                f"Average historical return is {avg_return:.2f}%."
            )

        win_streak = historical.get("win_streak", 0)

        if win_streak >= 5:
            strengths.append(
                f"Current winning streak is {win_streak} trades."
            )

        confidence = historical.get("confidence", 0)

        if confidence >= 75:
            strengths.append(
                "Historical AI confidence is high."
            )

        return strengths


    # ============================================================
    # HISTORICAL RISKS
    # ============================================================

    def _historical_risks(self, historical):

        risks = []

        if not historical:
            return risks

        drawdown = historical.get("max_drawdown", 0)

        if drawdown > 10:
            risks.append(
                f"Historical maximum drawdown is {drawdown:.2f}%."
            )

        loss_rate = historical.get("loss_rate", 0)

        if loss_rate > 35:
            risks.append(
                f"Historical loss rate is relatively high ({loss_rate:.1f}%)."
            )

        consecutive_losses = historical.get("losing_streak", 0)

        if consecutive_losses >= 3:
            risks.append(
                f"Recent losing streak consists of {consecutive_losses} trades."
            )

        return risks


    # ============================================================
    # TECHNICAL STRENGTHS
    # ============================================================

    def _technical_strengths(self, technical):

        strengths = []

        if not technical:
            return strengths

        rsi = technical.get("rsi")

        if rsi is not None:

            if 50 <= rsi <= 65:
                strengths.append(
                    f"RSI ({rsi:.2f}) confirms healthy bullish momentum."
                )

        ema = technical.get("ema_signal")

        if ema == "bullish":
            strengths.append(
                "Fast EMA is above Slow EMA."
            )

        macd = technical.get("macd_signal")

        if macd == "bullish":
            strengths.append(
                "MACD bullish crossover detected."
            )

        supertrend = technical.get("supertrend")

        if supertrend == "buy":
            strengths.append(
                "SuperTrend indicates BUY."
            )

        adx = technical.get("adx", 0)

        if adx >= 25:
            strengths.append(
                f"ADX ({adx:.2f}) indicates a strong trend."
            )

        volume = technical.get("volume_ratio", 1)

        if volume >= 1.5:
            strengths.append(
                f"Volume is {volume:.2f}x higher than average."
            )

        breakout = technical.get("breakout", False)

        if breakout:
            strengths.append(
                "Price has broken above resistance."
            )

        above_vwap = technical.get("above_vwap", False)

        if above_vwap:
            strengths.append(
                "Price is trading above VWAP."
            )

        bullish_pattern = technical.get("bullish_pattern")

        if bullish_pattern:
            strengths.append(
                f"Bullish candlestick pattern detected ({bullish_pattern})."
            )

        return strengths


    # ============================================================
    # TECHNICAL WEAKNESSES
    # ============================================================

    def _technical_weaknesses(self, technical):

        weaknesses = []

        if not technical:
            return weaknesses

        rsi = technical.get("rsi")

        if rsi is not None:

            if rsi > 75:
                weaknesses.append(
                    f"RSI ({rsi:.2f}) indicates overbought conditions."
                )

            elif rsi < 30:
                weaknesses.append(
                    f"RSI ({rsi:.2f}) indicates oversold conditions."
                )

        macd = technical.get("macd_signal")

        if macd == "bearish":
            weaknesses.append(
                "MACD bearish crossover detected."
            )

        ema = technical.get("ema_signal")

        if ema == "bearish":
            weaknesses.append(
                "Fast EMA remains below Slow EMA."
            )

        below_vwap = technical.get("below_vwap", False)

        if below_vwap:
            weaknesses.append(
                "Price is trading below VWAP."
            )

        atr = technical.get("atr_percent", 0)

        if atr > 5:
            weaknesses.append(
                f"ATR ({atr:.2f}%) indicates elevated volatility."
            )

        bearish_pattern = technical.get("bearish_pattern")

        if bearish_pattern:
            weaknesses.append(
                f"Bearish candlestick pattern detected ({bearish_pattern})."
            )

        return weaknesses



    # ============================================================
    # MARKET STRENGTHS
    # ============================================================

    def _market_strengths(self, market):

        strengths = []

        if not market:
            return strengths

        regime = market.get("market_regime", "").lower()

        if regime in ("bull", "bullish"):
            strengths.append(
                "Overall market regime is bullish."
            )

        trend = market.get("trend", "").lower()

        if trend == "uptrend":
            strengths.append(
                "Market is in a confirmed uptrend."
            )

        sector_strength = market.get("sector_strength", 0)

        if sector_strength >= 75:
            strengths.append(
                f"Sector strength is very strong ({sector_strength:.1f})."
            )

        relative_strength = market.get("relative_strength", 0)

        if relative_strength >= 80:
            strengths.append(
                f"Stock is outperforming peers (RS={relative_strength:.1f})."
            )

        support = market.get("near_support", False)

        if support:
            strengths.append(
                "Price is trading near a strong support zone."
            )

        resistance_break = market.get("resistance_breakout", False)

        if resistance_break:
            strengths.append(
                "Resistance breakout has been confirmed."
            )

        higher_highs = market.get("higher_highs", False)

        if higher_highs:
            strengths.append(
                "Price continues to form higher highs."
            )

        higher_lows = market.get("higher_lows", False)

        if higher_lows:
            strengths.append(
                "Price continues to form higher lows."
            )

        mtf = market.get("multi_timeframe_alignment", False)

        if mtf:
            strengths.append(
                "Trend is aligned across multiple timeframes."
            )

        institutional = market.get("institutional_buying", False)

        if institutional:
            strengths.append(
                "Institutional buying activity detected."
            )

        return strengths


    # ============================================================
    # MARKET RISKS
    # ============================================================

    def _market_risks(self, market):

        risks = []

        if not market:
            return risks

        regime = market.get("market_regime", "").lower()

        if regime in ("bear", "bearish"):
            risks.append(
                "Overall market regime is bearish."
            )

        trend = market.get("trend", "").lower()

        if trend == "downtrend":
            risks.append(
                "Market is currently in a downtrend."
            )

        resistance = market.get("near_resistance", False)

        if resistance:
            risks.append(
                "Price is approaching a major resistance zone."
            )

        weak_sector = market.get("sector_strength", 100)

        if weak_sector < 40:
            risks.append(
                f"Sector strength is weak ({weak_sector:.1f})."
            )

        weak_rs = market.get("relative_strength", 100)

        if weak_rs < 40:
            risks.append(
                f"Relative strength is weak ({weak_rs:.1f})."
            )

        lower_highs = market.get("lower_highs", False)

        if lower_highs:
            risks.append(
                "Lower highs indicate weakening momentum."
            )

        lower_lows = market.get("lower_lows", False)

        if lower_lows:
            risks.append(
                "Lower lows indicate bearish price structure."
            )

        failed_breakout = market.get("failed_breakout", False)

        if failed_breakout:
            risks.append(
                "Recent breakout attempt has failed."
            )

        distribution = market.get("distribution_phase", False)

        if distribution:
            risks.append(
                "Distribution phase detected."
            )

        volatility = market.get("volatility", 0)

        if volatility > 35:
            risks.append(
                f"Market volatility is elevated ({volatility:.2f})."
            )

        return risks


    # ============================================================
    # OPTION STRENGTHS
    # ============================================================

    def _option_strengths(self, options):

        strengths = []

        if not options:
            return strengths

        pcr = options.get("pcr")

        if pcr is not None and 0.8 <= pcr <= 1.2:
            strengths.append(
                f"PCR ({pcr:.2f}) indicates balanced positioning."
            )

        oi = options.get("oi_buildup", "").lower()

        if oi == "long_buildup":
            strengths.append(
                "Long build-up detected in derivatives."
            )

        iv = options.get("iv_percentile", 0)

        if iv < 40:
            strengths.append(
                "Implied volatility is relatively low."
            )

        max_pain = options.get("near_max_pain", False)

        if max_pain:
            strengths.append(
                "Price is near Max Pain level."
            )

        call_unwind = options.get("call_unwinding", False)

        if call_unwind:
            strengths.append(
                "Call unwinding supports further upside."
            )

        put_write = options.get("put_writing", False)

        if put_write:
            strengths.append(
                "Aggressive put writing indicates bullish sentiment."
            )

        return strengths


    # ============================================================
    # OPTION RISKS
    # ============================================================

    def _option_risks(self, options):

        risks = []

        if not options:
            return risks

        pcr = options.get("pcr")

        if pcr is not None:

            if pcr < 0.6:
                risks.append(
                    f"PCR ({pcr:.2f}) indicates excessive bullish positioning."
                )

            elif pcr > 1.5:
                risks.append(
                    f"PCR ({pcr:.2f}) indicates excessive bearish positioning."
                )

        oi = options.get("oi_buildup", "").lower()

        if oi == "short_buildup":
            risks.append(
                "Short build-up detected."
            )

        iv = options.get("iv_percentile", 0)

        if iv > 80:
            risks.append(
                "Implied volatility is extremely high."
            )

        call_write = options.get("heavy_call_writing", False)

        if call_write:
            risks.append(
                "Heavy call writing may cap upside."
            )

        put_unwind = options.get("put_unwinding", False)

        if put_unwind:
            risks.append(
                "Put unwinding suggests weakening support."
            )

        return risks


    # ============================================================
    # EXECUTION PLAN
    # ============================================================

    def _execution(self, strategy, portfolio):

        execution = []

        if strategy:

            strategy_name = strategy.get("name") or strategy.get("strategy")

            if strategy_name:
                execution.append(
                    f"Recommended strategy: {strategy_name}."
                )

            timeframe = strategy.get("timeframe")

            if timeframe:
                execution.append(
                    f"Preferred timeframe: {timeframe}."
                )

            entry = strategy.get("entry")

            if entry:
                execution.append(
                    f"Enter near ₹{entry}."
                )

            stop = strategy.get("stop_loss")

            if stop:
                execution.append(
                    f"Stop Loss: ₹{stop}."
                )

            target = strategy.get("target")

            if target:
                execution.append(
                    f"Primary Target: ₹{target}."
                )

            rr = strategy.get("risk_reward")

            if rr:
                execution.append(
                    f"Risk Reward Ratio: {rr}:1."
                )

        if portfolio:

            allocation = portfolio.get("capital_allocation")

            if allocation:
                execution.append(
                    f"Allocate approximately {allocation}% of capital."
                )

            quantity = portfolio.get("quantity")

            if quantity:
                execution.append(
                    f"Suggested quantity: {quantity} shares."
                )

        if not execution:

            execution.extend([
                "Wait for entry confirmation.",
                "Use a limit order.",
                "Respect stop loss.",
                "Book partial profits at target levels."
            ])

        return execution


    # ============================================================
    # MONITORING CHECKLIST
    # ============================================================

    def _monitoring(self, technical, options):

        monitoring = []

        monitoring.append(
            "Monitor overall market trend."
        )

        monitoring.append(
            "Watch for unusual volume."
        )

        if technical:

            rsi = technical.get("rsi")

            if rsi is not None:
                monitoring.append(
                    f"Monitor RSI (Current: {rsi:.2f})."
                )

            adx = technical.get("adx")

            if adx:
                monitoring.append(
                    f"Track ADX strength ({adx:.2f})."
                )

            atr = technical.get("atr_percent")

            if atr:
                monitoring.append(
                    f"Watch ATR ({atr:.2f}%)."
                )

        if options:

            pcr = options.get("pcr")

            if pcr is not None:
                monitoring.append(
                    f"Monitor PCR ({pcr:.2f})."
                )

            iv = options.get("iv_percentile")

            if iv:
                monitoring.append(
                    f"Track IV Percentile ({iv:.2f})."
                )

            monitoring.append(
                "Monitor Open Interest changes."
            )

        monitoring.extend([
            "Track news events.",
            "Review sector performance.",
            "Observe institutional activity."
        ])

        return monitoring


    # ============================================================
    # AI REASONING
    # ============================================================

    def _ai_reasoning(
        self,
        historical,
        technical,
        market,
        strategy,
        options,
    ):

        reasoning = []

        # ---------------------------------
        # Historical
        # ---------------------------------

        if historical:

            sr = historical.get("success_rate")

            if sr:

                reasoning.append(
                    f"Historical model shows {sr:.1f}% success rate."
                )

        # ---------------------------------
        # Technical
        # ---------------------------------

        if technical:

            score = technical.get("score")

            if score:

                reasoning.append(
                    f"Technical score = {score:.1f}."
                )

            trend = technical.get("trend")

            if trend:

                reasoning.append(
                    f"Trend detected as {trend}."
                )

            pattern = technical.get("bullish_pattern")

            if pattern:

                reasoning.append(
                    f"Candlestick confirmation: {pattern}."
                )

        # ---------------------------------
        # Market
        # ---------------------------------

        if market:

            regime = market.get("market_regime")

            if regime:

                reasoning.append(
                    f"Market regime: {regime}."
                )

            sector = market.get("sector_strength")

            if sector:

                reasoning.append(
                    f"Sector strength score: {sector:.1f}."
                )

        # ---------------------------------
        # Options
        # ---------------------------------

        if options:

            pcr = options.get("pcr")

            if pcr is not None:

                reasoning.append(
                    f"PCR = {pcr:.2f}."
                )

            oi = options.get("oi_buildup")

            if oi:

                reasoning.append(
                    f"OI Build-up: {oi}."
                )

        # ---------------------------------
        # Strategy
        # ---------------------------------

        if strategy:

            name = strategy.get("name") or strategy.get("strategy")

            if name:

                reasoning.append(
                    f"Selected strategy: {name}."
                )

        reasoning.append(
            "Final recommendation is generated after combining historical, technical, market, options, and strategy signals."
        )

        return reasoning


    # ============================================================
    # EXPORT METHODS
    # ============================================================

    @staticmethod
    def export(explanation):

        return asdict(explanation)


    def to_dict(self, explanation):

        return asdict(explanation)


    def to_json(self, explanation):

        import json

        return json.dumps(
            asdict(explanation),
            indent=4,
            default=str
        )


    def pretty_print(self, explanation):

        print("=" * 80)

        print("TRADE EXPLANATION")

        print("=" * 80)

        print(f"Symbol         : {explanation.symbol}")
        print(f"Recommendation : {explanation.recommendation}")
        print(f"Confidence     : {explanation.confidence:.2f}%")
        print(f"Overall Score  : {explanation.overall_score}")

        print("\nSUMMARY")
        print(explanation.summary)

        print("\nSTRENGTHS")
        for item in explanation.strengths:
            print(f"  ✓ {item}")

        print("\nWEAKNESSES")
        for item in explanation.weaknesses:
            print(f"  • {item}")

        print("\nRISKS")
        for item in explanation.risks:
            print(f"  ⚠ {item}")

        print("\nEXECUTION PLAN")
        for item in explanation.execution_plan:
            print(f"  → {item}")

        print("\nMONITORING")
        for item in explanation.monitoring_points:
            print(f"  → {item}")

        print("\nAI REASONING")
        for item in explanation.ai_reasoning:
            print(f"  • {item}")

        print("=" * 80)


    # ============================================================
    # EVIDENCE ENGINE
    # ============================================================

    def _evidence_analysis(self, evidence):

        explanations = []

        if not evidence:
            return explanations

        score = evidence.get("score", 0)

        explanations.append(
            f"Evidence Score : {score:.2f}"
        )

        bullish = evidence.get("bullish_evidence", [])

        for item in bullish:
            explanations.append(f"Bullish Evidence : {item}")

        bearish = evidence.get("bearish_evidence", [])

        for item in bearish:
            explanations.append(f"Bearish Evidence : {item}")

        missing = evidence.get("missing_confirmation", [])

        for item in missing:
            explanations.append(f"Missing Confirmation : {item}")

        confidence = evidence.get("confidence")

        if confidence:
            explanations.append(
                f"Evidence Confidence : {confidence:.2f}%"
            )

        return explanations


    # ============================================================
    # RULE ENGINE
    # ============================================================

    def _rule_analysis(self, rules):

        explanation = []

        if not rules:
            return explanation

        passed = rules.get("passed_rules", [])

        failed = rules.get("failed_rules", [])

        for rule in passed:
            explanation.append(
                f"PASS : {rule}"
            )

        for rule in failed:
            explanation.append(
                f"FAIL : {rule}"
            )

        total = len(passed) + len(failed)

        if total:

            explanation.append(
                f"Rules Passed : {len(passed)}/{total}"
            )

        return explanation


    # ============================================================
    # FACTOR ENGINE
    # ============================================================

    def _factor_analysis(self, factors):

        explanation = []

        if not factors:
            return explanation

        for factor, score in factors.items():

            if isinstance(score, (int, float)):

                explanation.append(
                    f"{factor} : {score:.2f}"
                )

        return explanation


    # ============================================================
    # AI SCORE ENGINE
    # ============================================================

    def _ai_score_analysis(self, ai_score):

        explanation = []

        if not ai_score:
            return explanation

        final_score = ai_score.get("final_score", 0)

        explanation.append(
            f"Final AI Score : {final_score:.2f}"
        )

        confidence = ai_score.get("confidence")

        if confidence:

            explanation.append(
                f"AI Confidence : {confidence:.2f}%"
            )

        grade = ai_score.get("grade")

        if grade:

            explanation.append(
                f"Grade : {grade}"
            )

        recommendation = ai_score.get("recommendation")

        if recommendation:

            explanation.append(
                f"AI Recommendation : {recommendation}"
            )

        return explanation


    # ============================================================
    # RANKING ENGINE
    # ============================================================

    def _ranking_analysis(self, ranking):

        explanation = []

        if not ranking:
            return explanation

        rank = ranking.get("rank")

        total = ranking.get("total_candidates")

        if rank and total:

            explanation.append(
                f"Ranked #{rank} out of {total} candidates."
            )

        percentile = ranking.get("percentile")

        if percentile:

            explanation.append(
                f"Top {100-percentile:.1f}% candidate."
            )

        category = ranking.get("category")

        if category:

            explanation.append(
                f"Category : {category}"
            )

        return explanation


    # ============================================================
    # NEWS ANALYSIS
    # ============================================================

    def _news_analysis(self, news):

        explanation = []

        if not news:
            return explanation

        sentiment = news.get("sentiment", "").lower()

        score = news.get("score", 0)

        if sentiment:

            explanation.append(
                f"News Sentiment : {sentiment.title()}"
            )

        explanation.append(
            f"Sentiment Score : {score:.2f}"
        )

        headlines = news.get("top_headlines", [])

        for headline in headlines[:5]:
            explanation.append(
                f"• {headline}"
            )

        return explanation


    # ============================================================
    # FINAL RECOMMENDATION
    # ============================================================

    def _recommendation_summary(

        self,

        decision,

        confidence,

        ai_score,

    ):

        summary = []

        recommendation = decision.get(
            "recommendation",
            "WATCH"
        )

        score = ai_score.get(
            "final_score",
            0
        )

        conf = confidence.get(
            "confidence",
            0
        )

        summary.append(
            f"Recommendation : {recommendation}"
        )

        summary.append(
            f"AI Score : {score:.2f}"
        )

        summary.append(
            f"Confidence : {conf:.2f}%"
        )

        if score >= 90:

            summary.append(
                "Exceptional high-conviction opportunity."
            )

        elif score >= 80:

            summary.append(
                "Strong candidate for execution."
            )

        elif score >= 70:

            summary.append(
                "Good candidate with moderate conviction."
            )

        elif score >= 60:

            summary.append(
                "Watch closely for confirmation."
            )

        else:

            summary.append(
                "Avoid until stronger confirmation."
            )

        return summary



    # ============================================================
    # PORTFOLIO ANALYSIS
    # ============================================================

    def _portfolio_analysis(self, portfolio):

        explanation = []

        if not portfolio:
            return explanation

        capital = portfolio.get("capital")

        if capital:
            explanation.append(
                f"Available Capital : ₹{capital:,.2f}"
            )

        allocation = portfolio.get("capital_allocation")

        if allocation:
            explanation.append(
                f"Capital Allocation : {allocation:.2f}%"
            )

        invested = portfolio.get("invested_amount")

        if invested:
            explanation.append(
                f"Investment Amount : ₹{invested:,.2f}"
            )

        quantity = portfolio.get("quantity")

        if quantity:
            explanation.append(
                f"Recommended Quantity : {quantity}"
            )

        diversification = portfolio.get("diversification_score")

        if diversification:
            explanation.append(
                f"Diversification Score : {diversification:.2f}"
            )

        exposure = portfolio.get("sector_exposure")

        if exposure:
            explanation.append(
                f"Sector Exposure : {exposure:.2f}%"
            )

        return explanation


    # ============================================================
    # POSITION SIZING
    # ============================================================

    def _position_size_analysis(self, portfolio):

        explanation = []

        if not portfolio:
            return explanation

        risk_percent = portfolio.get("risk_per_trade")

        if risk_percent:

            explanation.append(
                f"Risk Per Trade : {risk_percent:.2f}%"
            )

        stop = portfolio.get("stop_loss")

        if stop:

            explanation.append(
                f"Stop Loss Price : ₹{stop}"
            )

        risk_amount = portfolio.get("risk_amount")

        if risk_amount:

            explanation.append(
                f"Maximum Risk : ₹{risk_amount:,.2f}"
            )

        reward = portfolio.get("expected_reward")

        if reward:

            explanation.append(
                f"Expected Reward : ₹{reward:,.2f}"
            )

        return explanation


    # ============================================================
    # RISK MANAGEMENT
    # ============================================================

    def _risk_management(self, strategy, portfolio):

        explanation = []

        stop = strategy.get("stop_loss")

        if stop:

            explanation.append(
                f"Hard Stop Loss : ₹{stop}"
            )

        trailing = strategy.get("trailing_stop")

        if trailing:

            explanation.append(
                f"Trailing Stop : {trailing}%"
            )

        breakeven = strategy.get("move_to_breakeven")

        if breakeven:

            explanation.append(
                "Move stop loss to breakeven after first target."
            )

        max_loss = portfolio.get("risk_amount")

        if max_loss:

            explanation.append(
                f"Maximum Capital at Risk : ₹{max_loss:,.2f}"
            )

        return explanation


    # ============================================================
    # TRADE LIFECYCLE
    # ============================================================

    def _trade_lifecycle(self, strategy):

        lifecycle = []

        lifecycle.append(
            "1. Wait for entry confirmation."
        )

        lifecycle.append(
            "2. Enter using limit order."
        )

        lifecycle.append(
            "3. Confirm volume expansion."
        )

        lifecycle.append(
            "4. Maintain predefined stop loss."
        )

        lifecycle.append(
            "5. Book partial profits at Target 1."
        )

        lifecycle.append(
            "6. Trail remaining position."
        )

        lifecycle.append(
            "7. Exit on reversal confirmation."
        )

        return lifecycle


    # ============================================================
    # RISK SCORE
    # ============================================================

    def _risk_score(self, technical, market, options):

        score = 0

        if technical.get("rsi", 50) > 75:
            score += 10

        if market.get("market_regime") == "bearish":
            score += 20

        if options.get("iv_percentile", 0) > 80:
            score += 15

        if technical.get("atr_percent", 0) > 5:
            score += 10

        if market.get("volatility", 0) > 35:
            score += 20

        return min(score, 100)


    # ============================================================
    # CONVICTION LEVEL
    # ============================================================

    def _conviction_level(self, ai_score, confidence):

        score = ai_score.get("final_score", 0)

        conf = confidence.get("confidence", 0)

        overall = (score + conf) / 2

        if overall >= 90:
            return "Very High Conviction"

        if overall >= 80:
            return "High Conviction"

        if overall >= 70:
            return "Moderate Conviction"

        if overall >= 60:
            return "Low Conviction"

        return "Very Low Conviction"


    # ============================================================
    # FINAL CHECKLIST
    # ============================================================

    def _execution_checklist(self):

        return [

            "✔ Market trend confirmed",

            "✔ Volume confirmed",

            "✔ Technical confirmation available",

            "✔ Risk Reward acceptable",

            "✔ Stop Loss defined",

            "✔ Position size calculated",

            "✔ Capital allocation verified",

            "✔ News checked",

            "✔ Sector strength confirmed",

            "✔ Option chain validated",

            "✔ AI score above threshold",

            "✔ Confidence above threshold"

        ]


    # ============================================================
    # PORTFOLIO ANALYSIS
    # ============================================================

    def _portfolio_analysis(self, portfolio):

        explanation = []

        if not portfolio:
            return explanation

        capital = portfolio.get("capital")

        if capital:
            explanation.append(
                f"Available Capital : ₹{capital:,.2f}"
            )

        allocation = portfolio.get("capital_allocation")

        if allocation:
            explanation.append(
                f"Capital Allocation : {allocation:.2f}%"
            )

        invested = portfolio.get("invested_amount")

        if invested:
            explanation.append(
                f"Investment Amount : ₹{invested:,.2f}"
            )

        quantity = portfolio.get("quantity")

        if quantity:
            explanation.append(
                f"Recommended Quantity : {quantity}"
            )

        diversification = portfolio.get("diversification_score")

        if diversification:
            explanation.append(
                f"Diversification Score : {diversification:.2f}"
            )

        exposure = portfolio.get("sector_exposure")

        if exposure:
            explanation.append(
                f"Sector Exposure : {exposure:.2f}%"
            )

        return explanation


    # ============================================================
    # POSITION SIZING
    # ============================================================

    def _position_size_analysis(self, portfolio):

        explanation = []

        if not portfolio:
            return explanation

        risk_percent = portfolio.get("risk_per_trade")

        if risk_percent:

            explanation.append(
                f"Risk Per Trade : {risk_percent:.2f}%"
            )

        stop = portfolio.get("stop_loss")

        if stop:

            explanation.append(
                f"Stop Loss Price : ₹{stop}"
            )

        risk_amount = portfolio.get("risk_amount")

        if risk_amount:

            explanation.append(
                f"Maximum Risk : ₹{risk_amount:,.2f}"
            )

        reward = portfolio.get("expected_reward")

        if reward:

            explanation.append(
                f"Expected Reward : ₹{reward:,.2f}"
            )

        return explanation


    # ============================================================
    # RISK MANAGEMENT
    # ============================================================

    def _risk_management(self, strategy, portfolio):

        explanation = []

        stop = strategy.get("stop_loss")

        if stop:

            explanation.append(
                f"Hard Stop Loss : ₹{stop}"
            )

        trailing = strategy.get("trailing_stop")

        if trailing:

            explanation.append(
                f"Trailing Stop : {trailing}%"
            )

        breakeven = strategy.get("move_to_breakeven")

        if breakeven:

            explanation.append(
                "Move stop loss to breakeven after first target."
            )

        max_loss = portfolio.get("risk_amount")

        if max_loss:

            explanation.append(
                f"Maximum Capital at Risk : ₹{max_loss:,.2f}"
            )

        return explanation


    # ============================================================
    # TRADE LIFECYCLE
    # ============================================================

    def _trade_lifecycle(self, strategy):

        lifecycle = []

        lifecycle.append(
            "1. Wait for entry confirmation."
        )

        lifecycle.append(
            "2. Enter using limit order."
        )

        lifecycle.append(
            "3. Confirm volume expansion."
        )

        lifecycle.append(
            "4. Maintain predefined stop loss."
        )

        lifecycle.append(
            "5. Book partial profits at Target 1."
        )

        lifecycle.append(
            "6. Trail remaining position."
        )

        lifecycle.append(
            "7. Exit on reversal confirmation."
        )

        return lifecycle


    # ============================================================
    # RISK SCORE
    # ============================================================

    def _risk_score(self, technical, market, options):

        score = 0

        if technical.get("rsi", 50) > 75:
            score += 10

        if market.get("market_regime") == "bearish":
            score += 20

        if options.get("iv_percentile", 0) > 80:
            score += 15

        if technical.get("atr_percent", 0) > 5:
            score += 10

        if market.get("volatility", 0) > 35:
            score += 20

        return min(score, 100)


    # ============================================================
    # CONVICTION LEVEL
    # ============================================================

    def _conviction_level(self, ai_score, confidence):

        score = ai_score.get("final_score", 0)

        conf = confidence.get("confidence", 0)

        overall = (score + conf) / 2

        if overall >= 90:
            return "Very High Conviction"

        if overall >= 80:
            return "High Conviction"

        if overall >= 70:
            return "Moderate Conviction"

        if overall >= 60:
            return "Low Conviction"

        return "Very Low Conviction"


    # ============================================================
    # FINAL CHECKLIST
    # ============================================================

    def _execution_checklist(self):

        return [

            "✔ Market trend confirmed",

            "✔ Volume confirmed",

            "✔ Technical confirmation available",

            "✔ Risk Reward acceptable",

            "✔ Stop Loss defined",

            "✔ Position size calculated",

            "✔ Capital allocation verified",

            "✔ News checked",

            "✔ Sector strength confirmed",

            "✔ Option chain validated",

            "✔ AI score above threshold",

            "✔ Confidence above threshold"

        ]