
from consolidation_detector.base import ConsolidationScorer, FeatureType
import pandas as pd
import numpy as np
import logging

class ConsolidationManager:
    def __init__(self, scorers: list[ConsolidationScorer], weights=None):
        self.scorers = scorers
        self.weights = weights or [1] * len(scorers)
        if len(self.weights) != len(self.scorers):
            raise ValueError("Number of weights must match number of scorers")

    def compute_combined_score(self, data: pd.DataFrame) -> float:

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        scores = []
        for scorer in self.scorers:
            try:
                score = scorer.compute_score_feature_type(data, FeatureType.SCORE)
            except Exception as exc:
                logging.error("Scorer %s failed: %s", scorer.__class__.__name__, exc)
                score = 0.0
            scores.append(score)

        weighted = [s * w for s, w in zip(scores, self.weights)]
        try:

            denom = sum(self.weights)
            if denom == 0:
                raise ZeroDivisionError("Sum of weights is zero")
            combined = sum(weighted) / denom

        except Exception as exc:
            logging.exception("Failed to compute combined score: %s", exc)
            combined = 0.0

        return float(np.clip(combined, 0, 1))
