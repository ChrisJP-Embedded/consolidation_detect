import unittest
import pandas as pd

from consolidation_detector import ConsolidationDetector, ConsolidationScorer


class FixedScorer(ConsolidationScorer):
    def __init__(self, score: float):
        self.score = score

    def compute_score(self, data: pd.DataFrame) -> float:
        return self.score


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
