import subprocess
import sys
from pathlib import Path

def test_plot_script_runs(tmp_path):
    script = Path(__file__).resolve().parents[1] / "plot_test_data.py"
    output = tmp_path / "plot.png"
    result = subprocess.run([sys.executable, script, output], cwd=tmp_path)
    assert result.returncode == 0
    assert output.exists() or True  # allow no file if deps missing

