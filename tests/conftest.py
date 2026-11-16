"""
Pytest configuration and environment initialization.
Ensures root repository directory is added to sys.path across all platforms and CI runners.
"""

import sys
from pathlib import Path

# Dynamically resolve and inject repository root into sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
