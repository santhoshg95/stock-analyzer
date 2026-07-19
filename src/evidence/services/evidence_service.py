"""
Evidence Service

Converts intelligence modules into normalized evidence.
"""

from src.context.stock_context import StockContext

from src.evidence.models.evidence import Evidence
from src.evidence.models.evidence_collection import (
    EvidenceCollection,
)


class EvidenceService:
    """
    Collect evidence from all intelligence engines.
    """

    def collect(
        self,
        context: StockContext,
    ) -> EvidenceCollection:

        collection = EvidenceCollection()

        # ---------------------------------------------------
        # Options
        # ---------------------------------------------------

        if (
            context.options
            and context.options.analysis
        ):

            option = context.options.analysis

            collection.add(

                Evidence(

                    source="OPTIONS",

                    signal=option.status,

                    confidence=option.confidence,

                    weight=0.30,

                    score=option.score,

                    reason=", ".join(option.reasons),

                )

            )

        #
        # Technical
        #

        #
        # News
        #

        #
        # Market
        #

        return collection