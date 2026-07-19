"""
Open Interest Analysis Result
"""

from dataclasses import dataclass


@dataclass(slots=True)
class OIAnalysisResult:
    """
    Result of Open Interest analysis.
    """

    call_resistance: float | None

    put_support: float | None

    highest_call_oi: int

    highest_put_oi: int