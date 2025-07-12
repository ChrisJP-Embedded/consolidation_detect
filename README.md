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
