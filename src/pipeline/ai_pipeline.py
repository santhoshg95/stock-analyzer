"""
AI Trading Pipeline

End-to-end orchestration layer.

Execution Flow

1. Download Historical Data
2. Historical Statistics
3. Historical Intelligence
4. Qualification
5. Ranking
6. Market Regime
7. Strategy Recommendation
8. Options Intelligence
9. Strategy Selection
10. Strike Optimization
11. Trade Planning
12. Decision Engine
13. Confidence Engine
14. Portfolio Optimization
15. Trade Explanation
"""

from __future__ import annotations

from typing import Dict, Any

from src.historical.repository import HistoricalRepository
from src.historical.statistics.statistics_engine import HistoricalStatisticsEngine
from src.historical.intelligence import HistoricalIntelligenceEngine
from src.historical.qualification import HistoricalQualificationEngine

from src.strategy.recommender import StrategyRecommendationEngine

from src.options.intelligence import OptionsIntelligenceEngine
from src.options.strategy_selector import OptionsStrategySelector
from src.options.strike_optimizer import StrikeOptimizer
from src.options.trade_planner import TradePlanner

from src.ai.market_regime import MarketRegimeEngine
from src.ai.decision_engine import DecisionEngine
from src.ai.confidence_engine import ConfidenceEngine
from src.ai.portfolio_optimizer import PortfolioOptimizer
from src.ai.trade_explainer import TradeExplainer


class AITradingPipeline:

    def __init__(self):

        self.repository = HistoricalRepository()

        self.statistics = HistoricalStatisticsEngine()

        self.intelligence = HistoricalIntelligenceEngine()

        self.qualification = HistoricalQualificationEngine()

        self.market = MarketRegimeEngine()

        self.strategy = StrategyRecommendationEngine()

        self.option_intelligence = OptionsIntelligenceEngine()

        self.option_selector = OptionsStrategySelector()

        self.optimizer = StrikeOptimizer()

        self.trade_planner = TradePlanner()

        self.decision = DecisionEngine()

        self.confidence = ConfidenceEngine()

        self.portfolio = PortfolioOptimizer(
            capital=100000
        )

        self.explainer = TradeExplainer()

    # ----------------------------------------------------------

    def run(

        self,

        symbol: str,

        indicators: Dict[str, Any],

        option_chain: Dict[str, Any],

    ) -> Dict[str, Any]:

        dataframe = self.repository.get_history(symbol)

        statistics = self.statistics.calculate(dataframe)

        intelligence = self.intelligence.from_dataframe(
            dataframe
        )

        qualification = self.qualification.qualify(
            intelligence
        )

        regime = self.market.evaluate(
            dataframe,
            indicators,
        )

        strategy = self.strategy.recommend(
            intelligence
        )

        option_analysis = self.option_intelligence.analyze(
            intelligence,
            option_chain,
        )

        option_strategy = self.option_selector.select(
            option_analysis
        )

        strike = self.optimizer.optimize(
            option_chain
        )

        trade_plan = self.trade_planner.create_plan(
            option_strategy,
            strike,
        )

        decision = self.decision.evaluate(
            historical_score=intelligence.overall_score,
            strategy_score=strategy.confidence,
            options_score=option_analysis.combined_score,
            market_score=regime.score,
        )

        confidence = self.confidence.evaluate(
            historical_score=intelligence.overall_score,
            strategy_score=strategy.confidence,
            market_score=regime.score,
            options_score=option_analysis.combined_score,
            liquidity_score=intelligence.liquidity_score,
            volatility_score=100 - intelligence.volatility,
            signal_agreement=80,
            prediction_accuracy=75,
        )

        portfolio = self.portfolio.optimize(
            [
                {
                    "symbol": symbol,
                    "confidence": confidence.confidence,
                    "expected_return": strike.expected_return,
                    "volatility": intelligence.volatility,
                    "price": dataframe.Close.iloc[-1],
                }
            ]
        )

        explanation = self.explainer.explain(

            symbol=symbol,

            historical=intelligence.__dict__,

            strategy=strategy.__dict__,

            options=option_analysis.__dict__,

            decision=decision.__dict__,

            confidence=confidence.__dict__,

            portfolio=self.portfolio.summary(
                portfolio
            ),

        )

        return {

            "qualification": qualification,

            "market_regime": regime,

            "historical": intelligence,

            "strategy": strategy,

            "options": option_analysis,

            "trade_plan": trade_plan,

            "decision": decision,

            "confidence": confidence,

            "portfolio": portfolio,

            "explanation": explanation,

        }