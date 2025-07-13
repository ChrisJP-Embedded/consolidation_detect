import unittest
import pandas as pd

from consolidation_detector import (
    ConsolidationDetector,
    ConsolidationScorer,
)


class FixedScorer(ConsolidationScorer):
    def __init__(self, score: float, window: int = 1):
        self.score = score
        self.window = window

    def _compute_score(self, data: pd.DataFrame) -> float:
        return self.score

    def get_required_window(self) -> int:
        return self.window


class TestConsolidationDetector(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({"close": [1, 2, 3]})

    def test_gte_detection(self):
        detector = ConsolidationDetector([FixedScorer(0.6)], threshold=0.5, comparison="gte")
        self.assertTrue(detector.detect(self.data))
        detector = ConsolidationDetector([FixedScorer(0.4)], threshold=0.5, comparison="gte")
        self.assertFalse(detector.detect(self.data))

    def test_lte_detection(self):
        detector = ConsolidationDetector([FixedScorer(0.4)], threshold=0.5, comparison="lte")
        self.assertTrue(detector.detect(self.data))
        detector = ConsolidationDetector([FixedScorer(0.6)], threshold=0.5, comparison="lte")
        self.assertFalse(detector.detect(self.data))


if __name__ == "__main__":
    unittest.main()
