"""
Sector Engine

Converts SectorStrength output into DecisionContext.
"""

from src.models.decision_context import DecisionContext
from src.sector.sector_mapper import SectorMapper
from src.sector.sector_strength import SectorStrength


class SectorEngine:

    def __init__(self):

        self.mapper = SectorMapper()

        self.strength = SectorStrength()

    # ---------------------------------------------------------

    def analyze(self, symbol: str):

        sector = self.mapper.get_sector(symbol)

        if sector is None:

            return DecisionContext(

                engine="SECTOR",

                status="UNKNOWN",

                score=0,

                confidence=0,

                reasons=["Sector mapping not found."],

                warnings=[],

                metadata={}

            )

        report = self.strength.analyze()

        if sector not in report:

            return DecisionContext(

                engine="SECTOR",

                status="UNKNOWN",

                score=0,

                confidence=0,

                reasons=[f"No live sector data available for {sector}."],

                warnings=[],

                metadata={
                    "sector": sector
                }

            )

        sector_data = report[sector]

        return DecisionContext(

            engine="SECTOR",

            status=sector_data["rating"],

            score=sector_data["score"],

            confidence=sector_data["score"],

            reasons=[
                f"{sector} sector is {sector_data['rating']} "
                f"({sector_data['change_percent']:.2f}%)."
            ],

            warnings=[],

            metadata={

                "sector": sector,

                "price": sector_data["price"],

                "change_percent": sector_data["change_percent"]

            }

        )