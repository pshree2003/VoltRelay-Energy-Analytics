"""Generate a data inventory table for the VoltRelay project.

The script loads all expected datasets using :pymod:`src.data_ingestion` and prints a
summary for each one.  It also writes a Markdown artifact ``data_inventory.md``
containing a compact table that can be included in reports.
"""

import sys
from pathlib import Path
import pandas as pd

# Ensure the repository root is on the Python path when this script is run
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.data_ingestion import get_all_datasets, dataset_summary, EXPECTED_ROWS

def format_memory(mb: float) -> str:
    """Return a human‑readable memory string (MiB with 2 decimal places)."""
    return f"{mb:,.2f} MiB"

def main() -> None:
    datasets = get_all_datasets()

    rows = []
    for name, df in datasets.items():
        summary = dataset_summary(df)
        mem = format_memory(summary["memory_mb"])
        shape = f"{summary['shape'][0]:,} x {summary['shape'][1]:,}"
        date_range = summary["date_range"]
        dr = f"{date_range[0].date()} – {date_range[1].date()}" if date_range else "—"
        expected = EXPECTED_ROWS.get(name, "?")
        rows.append({
            "Dataset": name,
            "Rows (actual)": f"{summary['shape'][0]:,}",
            "Rows (expected)": f"{expected:,}",
            "Columns": summary["shape"][1],
            "Memory": mem,
            "Date range": dr,
        })

    inventory_df = pd.DataFrame(rows).sort_values("Dataset")

    md_path = REPO_ROOT / "tables" / "data_inventory.md"
    md_path.parent.mkdir(parents=True, exist_ok=True)
    with md_path.open("w", encoding="utf-8") as f:
        f.write("# Data Inventory\n\n")
        f.write(inventory_df.to_markdown(index=False))
        f.write("\n")
    print("Data inventory written to:", md_path)
    print(inventory_df)

if __name__ == "__main__":
    main()
