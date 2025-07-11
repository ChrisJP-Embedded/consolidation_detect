
from consolidation_detector.base import ConsolidationScorer
import pandas as pd
import numpy as np

class BBWidthConsolidation(ConsolidationScorer):
    def __init__(self, period: int = 20, normalize_range=(0.0, 0.05)):
        self.period = period
        self.min_width, self.max_width = normalize_range

    def compute_score(self, data: pd.DataFrame) -> float:
        if len(data) < self.period:
            return 0.0

        rolling_mean = data['close'].rolling(self.period).mean()
        rolling_std = data['close'].rolling(self.period).std()

        upper_band = rolling_mean + 2 * rolling_std
        lower_band = rolling_mean - 2 * rolling_std

        width = (upper_band - lower_band) / rolling_mean
        current_width = width.iloc[-1]

        norm = np.clip((self.max_width - current_width) / (self.max_width - self.min_width), 0, 1)
        return norm
