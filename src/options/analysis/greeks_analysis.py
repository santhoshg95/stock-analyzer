"""
Greeks Analysis
"""

from src.options.models.greeks_analysis_result import GreeksAnalysisResult
from src.options.models.option_chain import OptionChain


class GreeksAnalysis:
    """
    Performs aggregate Greeks analysis across the option chain.
    """

    def analyze(self, chain: OptionChain) -> GreeksAnalysisResult:

        contracts = chain.calls + chain.puts

        deltas = [
            c.delta for c in contracts
            if c.delta is not None
        ]

        gammas = [
            c.gamma for c in contracts
            if c.gamma is not None
        ]

        thetas = [
            c.theta for c in contracts
            if c.theta is not None
        ]

        vegas = [
            c.vega for c in contracts
            if c.vega is not None
        ]

        rhos = [
            c.rho for c in contracts
            if c.rho is not None
        ]

        def average(values):

            if not values:
                return 0.0

            return round(sum(values) / len(values), 4)

        avg_delta = average(deltas)
        avg_gamma = average(gammas)
        avg_theta = average(thetas)
        avg_vega = average(vegas)
        avg_rho = average(rhos)

        confidence = 0

        reasons = []

        if deltas:

            confidence += 20
            reasons.append("Delta available.")

        if gammas:

            confidence += 20
            reasons.append("Gamma available.")

        if thetas:

            confidence += 20
            reasons.append("Theta available.")

        if vegas:

            confidence += 20
            reasons.append("Vega available.")

        if rhos:

            confidence += 20
            reasons.append("Rho available.")

        if avg_delta > 0.30:

            bias = "BULLISH"

        elif avg_delta < -0.30:

            bias = "BEARISH"

        else:

            bias = "NEUTRAL"

        return GreeksAnalysisResult(

            average_delta=avg_delta,

            average_gamma=avg_gamma,

            average_theta=avg_theta,

            average_vega=avg_vega,

            average_rho=avg_rho,

            confidence=confidence,

            market_bias=bias,

            reasons=reasons

        )