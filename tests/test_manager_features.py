import pandas as pd
import numpy as np
from consolidation_detector.manager import ConsolidationManager
from consolidation_detector.scorers.bb_width import BBWidthConsolidation
from consolidation_detector.base import FeatureType


def test_manager_feature_series_length():
    df = pd.DataFrame({"close": np.arange(30)})
    manager = ConsolidationManager([BBWidthConsolidation(period=5)])

    score_series = manager.compute_feature_series(df, FeatureType.SCORE)
    first_series = manager.compute_feature_series(df, FeatureType.FIRST_DERIV)
    second_series = manager.compute_feature_series(df, FeatureType.SECOND_DERIV)

    assert len(score_series) == len(df)
    assert len(first_series) == len(df)
    assert len(second_series) == len(df)


def test_manager_series_data_columns():
    df = pd.DataFrame({"close": np.arange(30)})
    manager = ConsolidationManager([BBWidthConsolidation(period=5)])

    df_feat = manager.compute_series_data(df)
    assert set(df_feat.columns) == {"score", "first_deriv", "second_deriv"}
    assert len(df_feat) == len(df)
