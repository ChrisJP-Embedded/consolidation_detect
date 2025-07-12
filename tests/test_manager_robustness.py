import unittest
import pandas as pd
import numpy as np

from consolidation_detector.manager import ConsolidationManager
from consolidation_detector.base import ConsolidationScorer
from consolidation_detector.scorers.bb_width import BBWidthConsolidation


class FailingScorer(ConsolidationScorer):
    def compute_score(self, data: pd.DataFrame) -> float:
        raise ValueError("failure")


class TestManagerRobustness(unittest.TestCase):
    def test_manager_handles_scorer_failure(self):
        df = pd.DataFrame({"close": np.arange(30)})
        manager = ConsolidationManager([
            BBWidthConsolidation(period=5),
            FailingScorer(),
        ])
        score = manager.compute_combined_score(df)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
