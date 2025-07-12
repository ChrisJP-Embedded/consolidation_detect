
import unittest
import pandas as pd
import numpy as np
from consolidation_detector.scorers.bb_width import BBWidthConsolidation


class TestBBWidth(unittest.TestCase):
    def test_bb_width(self):
        """BBWidthConsolidation returns a score between 0 and 1."""
        # Create fake data: trending interspersed with consolidation periods
        np.random.seed(0)
        trend1 = np.linspace(100, 110, 60)
        consolidation1 = np.ones(40) * 110 + np.random.normal(0, 0.2, 40)
        trend2 = np.linspace(110, 120, 60)
        consolidation2 = np.ones(40) * 120 + np.random.normal(0, 0.2, 40)
        trend3 = np.linspace(120, 130, 60)
        prices = np.concatenate([trend1, consolidation1, trend2, consolidation2, trend3])

        df = pd.DataFrame({
            "close": prices,
            "high": prices + 1,
            "low": prices - 1,
            "open": prices,
            "volume": np.random.randint(100, 200, len(prices)),
        })

        bb = BBWidthConsolidation(period=20)
        score = bb.compute_score(df)
        print(f"BB Width Score: {score}")
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()
