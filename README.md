# Consolidation Detector

This Python module detects **price consolidation phases** in time-series trading data. It uses **pluggable scorers** (like Bollinger Band width) to generate normalized consolidation scores and determine whether a market is in a consolidation state.

---

## 🔧 How It Works

The core of this system is modular:

### 1. Scorers
Each scorer implements a signal detection algorithm. It returns a **normalized score** (`0.0`–`1.0`) based on how "consolidated" the price data looks.

Example scorer:
- `BBWidthConsolidation`: Uses the width of Bollinger Bands to detect tight price ranges.

All scorers must inherit from `ConsolidationScorer` and implement:
```python
def compute_score(self, data: pd.DataFrame) -> float
```

### 2. Detector
The `ConsolidationDetector`:
- Accepts a list of scorers.
- Optionally uses weights to prioritize some scorers more than others.
- Computes a combined normalized score.
- Compares it to a threshold.
- Returns `True` if the score meets the condition.

---

## 🚀 Quick Start

```python
import pandas as pd
from consolidation_detector import ConsolidationDetector, BBWidthConsolidation

# Load or simulate price data
df = pd.DataFrame({"close": [100, 101, 100.5, 99.8, 100.1, 100.0, 100.1] * 3})

# Set up scorers
scorers = [BBWidthConsolidation(period=20)]

# Create detector
detector = ConsolidationDetector(scorers=scorers, threshold=0.8)

# Detect consolidation
result = detector.detect(df)

print(f"Consolidation detected? {result}")
```

---

## 🔍 Print Score for Debugging

To inspect the current normalized score instead of just the boolean result:

```python
from consolidation_detector.manager import ConsolidationManager

manager = ConsolidationManager(scorers)
score = manager.compute_combined_score(df)
print(f"Normalized score: {score:.4f}")
```

Or print per-scorer contributions:
```python
for scorer in scorers:
    print(f"{scorer.__class__.__name__}: {scorer.compute_score(df):.4f}")
```

---

## Requirements
- Python 3.11 or higher

We recommend using [Pipenv](https://pipenv.pypa.io/) for dependency management. After installing Python 3.11, set up the environment with:

```bash
pipenv install --dev
```

## Running Tests
Run the full test suite with:

```bash
python -m unittest discover -v
```

## Examples
The `examples` directory contains `plot_test_data.py` which demonstrates generating synthetic data and plotting consolidation scores.

## Consolidation Detection

Use `ConsolidationDetector` to check if prices are in consolidation based on a score threshold. Set `comparison` to `'gte'` (default) to detect scores greater than or equal to the threshold, or `'lte'` to detect scores less than or equal to it.

```python
from consolidation_detector import ConsolidationDetector, BBWidthConsolidation

scorers = [BBWidthConsolidation(period=20)]
detector = ConsolidationDetector(scorers, threshold=0.8, comparison="gte")

if detector.detect(price_dataframe):
    print("Consolidation detected")
```

