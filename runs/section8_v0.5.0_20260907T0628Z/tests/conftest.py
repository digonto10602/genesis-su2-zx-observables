import sys
from pathlib import Path

# Ensure RUN/src is on sys.path so `import su2qc...` works for all tests.
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
