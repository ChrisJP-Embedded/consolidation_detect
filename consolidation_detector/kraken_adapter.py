

import pandas as pd

def kraken_ohlc_to_df(ohlc_list):
    return pd.DataFrame(ohlc_list, columns=[
        "timestamp", "open", "high", "low", "close", "vwap", "volume", "count"
    ]).astype({
        "timestamp": "float64",
        "open": "float64",
        "high": "float64",
        "low": "float64",
        "close": "float64"
    })
