
from consolidation_detector.base import ConsolidationScorer
import pandas as pd
import numpy as np

class ConsolidationManager:
    def __init__(self, scorers: list[ConsolidationScorer], weights=None):
        self.scorers = scorers
        self.weights = weights or [1] * len(scorers)

    def compute_combined_score(self, data: pd.DataFrame) -> float:
        scores = [scorer.compute_score(data) for scorer in self.scorers]
        weighted = [s * w for s, w in zip(scores, self.weights)]
        return np.clip(sum(weighted) / sum(self.weights), 0, 1)
