"""Shared pytest configuration.

Ensures the project root is importable so `import app...` works when running
pytest locally as well as inside the Docker container.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
