from __future__ import annotations

from dataclasses import dataclass
from typing import List, Literal

import pandas as pd

from .base import ConsolidationScorer
from .manager import ConsolidationManager


Comparison = Literal["gte", "lte"]


@dataclass
class ConsolidationDetector:
    """Detect consolidation events based on a threshold."""

    scorers: List[ConsolidationScorer]
    threshold: float = 0.5
    comparison: Comparison = "gte"
    weights: List[float] | None = None

    def __post_init__(self) -> None:
        if self.comparison not in ("gte", "lte"):
            raise ValueError("comparison must be 'gte' or 'lte'")
        self.manager = ConsolidationManager(self.scorers, self.weights)

    def detect(self, data: pd.DataFrame) -> bool:
        """Return True if a consolidation event is detected."""
        score = self.manager.compute_combined_score(data)
        if self.comparison == "gte":
            return score >= self.threshold
        else:
            return score <= self.threshold
