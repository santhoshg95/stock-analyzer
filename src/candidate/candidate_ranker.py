"""
Candidate Ranker
"""

from typing import List

from src.models.candidate_result import CandidateResult


class CandidateRanker:

    @staticmethod
    def rank(results: List[CandidateResult]):

        return sorted(

            results,

            key=lambda x: x.score,

            reverse=True

        )