
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
        """Return the weighted normalized score."""
        return self.compute_combined_feature(data, FeatureType.SCORE)

    # New methods -----------------------------------------------------------

    def compute_combined_feature(
        self, data: pd.DataFrame, feature: FeatureType
    ) -> float:
        """Return weighted combined value for the given feature type."""

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        values: list[float] = []
        for scorer in self.scorers:
            try:
                value = scorer.compute_score_feature_type(data, feature)
            except Exception as exc:
                logging.error(
                    "Scorer %s failed: %s", scorer.__class__.__name__, exc
                )
                value = 0.0
            values.append(value)

        weighted = [v * w for v, w in zip(values, self.weights)]
        try:
            denom = sum(self.weights)
            if denom == 0:
                raise ZeroDivisionError("Sum of weights is zero")
            combined = sum(weighted) / denom
        except Exception as exc:
            logging.exception("Failed to compute combined feature: %s", exc)
            combined = 0.0

        return float(np.clip(combined, 0, 1)) if feature == FeatureType.SCORE else float(combined)

    def compute_feature_series(
        self, data: pd.DataFrame, feature: FeatureType
    ) -> pd.Series:
        """Return weighted time series for the given feature type."""

        if not isinstance(data, pd.DataFrame):
            raise TypeError("data must be a pandas DataFrame")

        series_list = []
        for scorer in self.scorers:
            try:
                base_series = scorer._compute_score_series(data)
                if feature == FeatureType.SCORE:
                    s = base_series
                elif feature == FeatureType.FIRST_DERIV:
                    s = base_series.diff()
                elif feature == FeatureType.SECOND_DERIV:
                    s = base_series.diff().diff()
                else:
                    raise ValueError(f"Unsupported FeatureType: {feature}")
            except Exception as exc:
                logging.error(
                    "Scorer %s failed: %s", scorer.__class__.__name__, exc
                )
                s = pd.Series(index=data.index, dtype=float)

            series_list.append(s)

        if not series_list:
            return pd.Series(dtype=float)

        df_all = pd.concat(series_list, axis=1)
        weighted = df_all.mul(self.weights, axis=1)
        denom = sum(self.weights)
        if denom == 0:
            logging.exception("Sum of weights is zero")
            return pd.Series(index=data.index, dtype=float)

        combined = weighted.sum(axis=1) / denom

        if feature == FeatureType.SCORE:
            combined = combined.clip(lower=0, upper=1)

        return combined

    def compute_series_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return DataFrame with score and derivative series for plotting."""

        return pd.DataFrame(
            {
                "score": self.compute_feature_series(data, FeatureType.SCORE),
                "first_deriv": self.compute_feature_series(
                    data, FeatureType.FIRST_DERIV
                ),
                "second_deriv": self.compute_feature_series(
                    data, FeatureType.SECOND_DERIV
                ),
            }
        )
