import os
import sys
import numpy as np
import pandas as pd

# Ensure the project package is importable when running this script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from consolidation_detector.scorers.bb_width import BBWidthConsolidation


def generate_test_data():
    """Return DataFrame with synthetic price data containing multiple consolidation phases."""
    np.random.seed(0)

    def trend(start, stop, length):
        return np.linspace(start, stop, length) + np.random.normal(0, 0.5, length)

    def consolidation(level, length):
        return np.full(length, level) + np.random.normal(0, 0.2, length)

    segments = [
        trend(100, 120, 80),
        consolidation(120, 30),
        trend(120, 90, 70),
        consolidation(90, 25),
        trend(90, 110, 60),
        consolidation(110, 35),
        trend(110, 95, 50),
        consolidation(95, 30),
        trend(95, 115, 70),
        consolidation(115, 40),
        trend(115, 100, 60),
        consolidation(100, 30),
    ]

    prices = np.concatenate(segments)
    df = pd.DataFrame({'close': prices})
    return df


def compute_scores(df, period=20):
    bb = BBWidthConsolidation(period=period)
    # Compute BB width score for each point using rolling window
    rolling_mean = df['close'].rolling(period).mean()
    rolling_std = df['close'].rolling(period).std()
    upper = rolling_mean + 2 * rolling_std
    lower = rolling_mean - 2 * rolling_std
    width = (upper - lower) / rolling_mean
    current = width
    score = np.clip((bb.max_width - current) / (bb.max_width - bb.min_width), 0, 1)
    return score


def main(output_file='consolidation_example.png'):
    import matplotlib.pyplot as plt
    df = generate_test_data()
    scores = compute_scores(df)

    plt.figure(figsize=(10, 4))
    plt.plot(df.index, df['close'], label='Close')
    plt.fill_between(df.index, df['close'].min(), df['close'].max(), where=scores > 0.8,
                     color='orange', alpha=0.3, label='Consolidation')
    plt.title('Synthetic Price Data with Consolidation Highlights')
    plt.xlabel('Index')
    plt.ylabel('Price')
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"Saved plot to {output_file}")


if __name__ == '__main__':
    main()
