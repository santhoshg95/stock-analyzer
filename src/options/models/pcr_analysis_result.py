"""
PCR Analysis Result
"""

from dataclasses import dataclass


@dataclass(slots=True)
class PCRAnalysisResult:
    """
    Result of Put Call Ratio analysis.
    """

    pcr: float

    sentiment: str

    total_call_oi: int

    total_put_oi: int