
import pandas as pd
import numpy as np
from consolidation_detector.scorers.bb_width import BBWidthConsolidation

def test_bb_width():
    # Create fake data: trending + consolidation
    np.random.seed(0)
    trend = np.linspace(100, 120, 100)
    consolidation = np.ones(50) * 120 + np.random.normal(0, 0.2, 50)
    prices = np.concatenate([trend, consolidation, trend])

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
    assert 0 <= score <= 1
