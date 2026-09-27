"""Config package for the VoltRelay analytics project.

Re‑exports the most commonly used objects from ``config.constants`` for
convenience when importing ``config``.  Also applies pandas display options
and ensures output directories exist at import time.
"""

from pathlib import Path
import pandas as pd

from .constants import (
    REPO_ROOT,
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    FIGURES_DIR,
    TABLES_DIR,
    REPORTS_DIR,
    PRESENTATION_DIR,
    NOTEBOOK_PATH,
    DISPLAY_MAX_ROWS,
    DISPLAY_MAX_COLUMNS,
)

# Apply display options at import time (useful for notebooks)
PANDAS_DISPLAY_OPTIONS = {
    "display.max_rows": DISPLAY_MAX_ROWS,
    "display.max_columns": DISPLAY_MAX_COLUMNS,
}
for key, val in PANDAS_DISPLAY_OPTIONS.items():
    pd.set_option(key, val)
pd.options.display.float_format = lambda x: f"{x:,.2f}"

# Ensure that output directories exist when the package is imported
for _dir in [FIGURES_DIR, TABLES_DIR, REPORTS_DIR, PRESENTATION_DIR, PROCESSED_DATA_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

__all__ = [
    "REPO_ROOT",
    "RAW_DATA_DIR",
    "PROCESSED_DATA_DIR",
    "FIGURES_DIR",
    "TABLES_DIR",
    "REPORTS_DIR",
    "PRESENTATION_DIR",
    "NOTEBOOK_PATH",
    "PANDAS_DISPLAY_OPTIONS",
]
