
import unittest
import pandas as pd
import numpy as np
from consolidation_detector.scorers.bb_width import BBWidthConsolidation
from examples.plot_test_data import generate_test_data

class TestBBWidth(unittest.TestCase):
    def test_bb_width(self):
        """BBWidthConsolidation returns a score between 0 and 1."""

        # Use synthetic data with multiple unique consolidation phases
        prices_df = generate_test_data()
        prices = prices_df['close'].to_numpy()
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
