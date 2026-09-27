import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any

from config import RAW_DATA_DIR

# Mapping of expected filenames to a friendly dataset name
DATASET_FILES = {
    "swap_events.csv": "swap_events",
    "station_hourly_status.csv": "station_hourly_status",
    "riders.csv": "riders",
    "batteries.csv": "batteries",
    "support_tickets.csv": "support_tickets",
    "stations.csv": "stations",
    "city_daily_context.csv": "city_daily_context",
    "fleet_partners.csv": "fleet_partners",
}

# Expected approximate row counts (for quick sanity check)
EXPECTED_ROWS: Dict[str, int] = {
    "swap_events": 3_877_013,
    "station_hourly_status": 1_487_712,
    "riders": 20_000,
    "batteries": 6_500,
    "support_tickets": 44_000,
    "stations": 152,
    "city_daily_context": 3_282,
    "fleet_partners": 12,
}

def _detect_date_columns(df: pd.DataFrame) -> List[str]:
    """Return column names that look like dates/times.
    Detects 'date', 'time', '_ts', and 'hour_start' (case‑insensitive).
    """
    return [c for c in df.columns if any(k in c.lower() for k in ["date", "time", "_ts", "hour_start"])]

def _load_large_csv(path: Path, dtype: Optional[Dict] = None) -> pd.DataFrame:
    """Load a large CSV using memory‑efficient options.
    - low_memory=False forces pandas to infer types in a single pass.
    - compression='infer' auto‑detects gzip/bz2/etc. from file extension.
    - specify dtype for identifier columns as string when caller provides it.
    """
    return pd.read_csv(
        path,
        compression="infer",
        low_memory=False,
        dtype=dtype,
        parse_dates=_detect_date_columns(pd.read_csv(path, nrows=0)),
    )

def _load_csv(path: Path, dtype: Optional[Dict] = None) -> pd.DataFrame:
    """Load a regular CSV (not gzipped)."""
    return pd.read_csv(
        path,
        dtype=dtype,
        parse_dates=_detect_date_columns(pd.read_csv(path, nrows=0)),
    )

def load_dataset(name: str) -> pd.DataFrame:
    """Load a dataset by its friendly name (e.g., ``swap_events``).

    * Validates that the underlying file exists under ``RAW_DATA_DIR``.
    * Preserves identifiers as strings – the caller may pass a ``dtype`` map via
      ``IDENTIFIER_COLUMNS``.
    * For large gzip files (``swap_events`` and ``station_hourly_status``) a
      memory‑efficient loader is used.
    """
    # Resolve filename
    filename = None
    for f, friendly in DATASET_FILES.items():
        if friendly == name:
            filename = f
            break
    if filename is None:
        raise ValueError(f"Unknown dataset name: {name!r}")

    file_path = RAW_DATA_DIR / filename
    if not file_path.is_file():
        raise FileNotFoundError(f"Expected data file not found: {file_path}")

    # Identify identifier columns – keep them as strings.
    # Simple heuristic: columns ending with "_id" or "id".
    sample_header = pd.read_csv(file_path, nrows=0, compression="infer")
    identifier_cols = [c for c in sample_header.columns if c.lower().endswith("_id") or c.lower() == "id"]
    dtype_map = {c: "string" for c in identifier_cols}

    # Use the large-CSV loader for datasets known to be big
    LARGE_DATASETS = {"swap_events", "station_hourly_status"}
    if name in LARGE_DATASETS:
        df = _load_large_csv(file_path, dtype=dtype_map)
    else:
        df = _load_csv(file_path, dtype=dtype_map)

    return df

def get_all_datasets() -> Dict[str, pd.DataFrame]:
    """Load **all** datasets and return a mapping ``name -> DataFrame``.
    """
    return {name: load_dataset(name) for name in EXPECTED_ROWS.keys()}

def dataset_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """Return a compact summary for a DataFrame.
    Includes shape, dtypes, memory usage (MiB) and, if there is a date column,
    the min / max values.
    """
    summary: Dict[str, Any] = {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": {c: str(dt) for c, dt in df.dtypes.items()},
        "memory_mb": df.memory_usage(deep=True).sum() / (1024 ** 2),
    }
    date_cols = [c for c, dt in df.dtypes.items() if pd.api.types.is_datetime64_any_dtype(dt)]
    if date_cols:
        col = date_cols[0]
        summary["date_range"] = (df[col].min(), df[col].max())
    else:
        summary["date_range"] = None
    return summary
