"""
Market Evidence
"""

from src.evidence.evidence import Evidence


class MarketEvidence:

    def build(self, context):

        result = []

        for reason in context.market.reasons:

            result.append(

                Evidence(

                    source="MARKET",

                    title="Market",

                    score=context.market.confidence,

                    confidence=context.market.confidence,

                    description=reason

                )

            )

        return result