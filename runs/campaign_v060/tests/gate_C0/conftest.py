import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
PACKAGE = REPO / "runs" / "section8_v0.5.0_20260907T0628Z" / "src"
sys.path.insert(0, str(PACKAGE))
