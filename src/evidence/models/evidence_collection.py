"""
Evidence Collection
"""

from dataclasses import dataclass, field

from src.evidence.models.evidence import Evidence


@dataclass(slots=True)
class EvidenceCollection:
    """
    Collection of evidence from all engines.
    """

    evidences: list[Evidence] = field(default_factory=list)

    def add(self, evidence: Evidence):

        self.evidences.append(evidence)

    @property
    def total_weight(self):

        return sum(
            evidence.weight
            for evidence in self.evidences
        )

    @property
    def weighted_score(self):

        if not self.evidences:
            return 0

        return sum(
            evidence.score * evidence.weight
            for evidence in self.evidences
        ) / self.total_weight