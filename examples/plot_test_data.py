import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from consolidation_detector.scorers.bb_width import BBWidthConsolidation


def generate_test_data():
    """Return DataFrame with synthetic price data containing two consolidation phases."""
    np.random.seed(0)
    trend1 = np.linspace(100, 110, 60)
    cons1 = np.ones(40) * 110 + np.random.normal(0, 0.2, 40)
    trend2 = np.linspace(110, 120, 60)
    cons2 = np.ones(40) * 120 + np.random.normal(0, 0.2, 40)
    trend3 = np.linspace(120, 130, 60)
    prices = np.concatenate([trend1, cons1, trend2, cons2, trend3])

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
