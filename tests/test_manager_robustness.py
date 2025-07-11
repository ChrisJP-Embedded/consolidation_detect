import pandas as pd
import numpy as np

from consolidation_detector.manager import ConsolidationManager
from consolidation_detector.base import ConsolidationScorer
from consolidation_detector.scorers.bb_width import BBWidthConsolidation


class FailingScorer(ConsolidationScorer):
    def compute_score(self, data: pd.DataFrame) -> float:
        raise ValueError("failure")


def test_manager_handles_scorer_failure():
    df = pd.DataFrame({"close": np.arange(30)})
    manager = ConsolidationManager([
        BBWidthConsolidation(period=5),
        FailingScorer(),
    ])
    score = manager.compute_combined_score(df)
    assert 0 <= score <= 1
