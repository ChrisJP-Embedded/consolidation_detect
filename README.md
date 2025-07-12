# Consolidation Detector

This project detects consolidation phases in price data using Bollinger Band widths and other scoring methods.

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

