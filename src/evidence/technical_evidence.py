"""
Technical Evidence
"""

from src.evidence.evidence import Evidence


class TechnicalEvidence:

    def build(self, context):

        result = []

        for reason in context.technical.reasons:

            result.append(

                Evidence(

                    source="TECHNICAL",

                    title="Technical",

                    score=context.technical.confidence,

                    confidence=context.technical.confidence,

                    description=reason

                )

            )

        return result