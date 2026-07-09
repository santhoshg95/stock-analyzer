"""
Evidence Engine
"""

from src.evidence.market_evidence import MarketEvidence
from src.evidence.technical_evidence import TechnicalEvidence


class EvidenceEngine:

    def __init__(self):

        self.engines = [

            MarketEvidence(),

            TechnicalEvidence()

        ]

    def collect(self, context):

        evidence = []

        for engine in self.engines:

            evidence.extend(

                engine.build(context)

            )

        return evidence