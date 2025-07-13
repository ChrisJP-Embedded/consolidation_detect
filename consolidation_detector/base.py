
from abc import ABC, abstractmethod
from enum import Enum
import pandas as pd
import numpy as np

class FeatureType(Enum):
    SCORE = 0              # Normalized primary score
    FIRST_DERIV = 1        # Rate of change
    SECOND_DERIV = 2       # Acceleration

class ConsolidationScorer(ABC):
    @abstractmethod
    def _compute_score(self, data: pd.DataFrame) -> float:
        """Compute the normalized score for the most recent frame"""
        pass

    def _compute_score_series(self, data: pd.DataFrame) -> pd.Series:
        """Compute normalized scores for each rolling window in the dataframe"""
        window = self.get_required_window()
        if len(data) < window:
            return pd.Series(dtype=float)

        return data.rolling(window=window).apply(
            lambda window_df: self._compute_score(window_df), raw=False
        )

    def compute_score_feature_type(self, data: pd.DataFrame, mode: FeatureType) -> float:
        """Return the normalized score or its first/second derivative"""
        if mode == FeatureType.SCORE:
            return self._compute_score(data)

        score_series = self._compute_score_series(data)
        if score_series.empty or score_series.isna().all():
            return 0.0

        score_series = score_series.dropna()

        if mode == FeatureType.FIRST_DERIV:
            diff = score_series.diff().dropna()
            return float(diff.iloc[-1]) if not diff.empty else 0.0
        elif mode == FeatureType.SECOND_DERIV:
            second_diff = score_series.diff().diff().dropna()
            return float(second_diff.iloc[-1]) if not second_diff.empty else 0.0
        else:
            raise ValueError(f"Unsupported FeatureType: {mode}")

    @abstractmethod
    def get_required_window(self) -> int:
        """Return the minimum window size needed for rolling score computation"""
        pass
