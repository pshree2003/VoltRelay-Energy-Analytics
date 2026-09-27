"""Project‑wide constants and configuration values.

All paths are defined relative to the repository root.  Using ``pathlib`` ensures
compatibility across operating systems (Windows, macOS, Linux).
"""

from pathlib import Path

# Repository root – adjust if this file is moved.
REPO_ROOT = Path(__file__).resolve().parent.parent

# Data directories
RAW_DATA_DIR = REPO_ROOT / "data" / "raw"
PROCESSED_DATA_DIR = REPO_ROOT / "data" / "processed"

# Output directories
FIGURES_DIR = REPO_ROOT / "figures"
TABLES_DIR = REPO_ROOT / "tables"
REPORTS_DIR = REPO_ROOT / "reports"
PRESENTATION_DIR = REPO_ROOT / "presentation"

# Notebook location
NOTEBOOK_PATH = REPO_ROOT / "notebooks" / "analysis.ipynb"

# Common settings
DISPLAY_MAX_ROWS = 20
DISPLAY_MAX_COLUMNS = 100

# Ensure output directories exist at runtime (no side‑effects when imported)
for _dir in [FIGURES_DIR, TABLES_DIR, REPORTS_DIR, PRESENTATION_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)
