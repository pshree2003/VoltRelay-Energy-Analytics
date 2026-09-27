# VoltRelay Energy: Reproducible Cleaning Audit & Transformation Log

**Pipeline Version**: 1.0 (Auditable & Reproducible)  
**Date**: 2026-09-27  
**Core Principle**: Raw data is never modified in-place. All transformations produce auxiliary calibrated fields and explicit validity flags.

---

## 1. Summary of Cleaning Actions and Records Impacted

| Dataset | Issue Identified | Detection Method | Records Affected | Transformation / Treatment | Business & Analytical Impact |
|:---|:---|:---|---:|:---|:---|
| `swap_events` | Firmware v3.2.0 clock drift | `station_firmware == 'v3.2.0'` & ts between 2025-03-10 and 2025-04-14 | **135,601** | Created `corrected_event_ts` (+5h 30m) & `timestamp_corrected_flag`. Raw `original_event_ts` preserved. | Prevents severe distortion of hour-of-day peak utilization and grid demand curves. |
| `riders` | Inconsistent `home_city` spellings | Exact match against known lowercase alias map | **585** | Created `clean_home_city` mapping 15+ variations to 6 canonical cities. `home_city` preserved. | Eliminates fragmentation in city-level cohort retention and revenue metrics. |
| `swap_events` | Packet re-transmission near-duplicates | Duplicate `(rider_id, station_id, event_ts)` under `offline_batch` | **26** | Tagged with `near_duplicate_flag`. Records retained for financial audit. | Prevents double-counting in operational throughput and failure counts. |
| `swap_events` | Negative / Outlier Odometer values | `km_since_last_swap < 0` or `> 500` | **36,096** | Created `valid_km_flag`. Raw values retained. | Prevents skew in average delivered range and vehicle efficiency calculations. |
| `swap_events` | SOC / SOH calibration drift (> 100%) | Sensor readings > 100.0% | **3,698** (SOC), **2,799** (SOH) | Created `calibrated_soc_out_pct`, `calibrated_soh_out_pct` clipped to 100.0%. Created validity flags. | Protects battery health degradation curves from false positive overcharging anomalies. |
| `stations` | Test station transactions | `station_id` containing `'TST'` (`STN-TST-01`, `STN-TST-02`) | **62,031** swaps | Tagged with `is_test_station_flag`. | Separates non-commercial R&D/benchmarking load from commercial network SLAs. |
| `station_hourly_status` | Missing station telemetry | `telemetry_status != 'ok'` | **9,384** hours | Strictly preserved as `NaN` (no zero-imputation). | Avoids artificial skew in ambient/cabinet temperatures and charging times. |
| `support_tickets` | CSAT missingness | `csat_score.isna()` | **28,871** (65.6%) | Flagged with `has_csat_rating`; missingness preserved. | Enables analysis of non-response bias between resolved and unresolved riders. |

---

## 2. Verification of Zero Raw Record Deletion
- Raw swap events input count: **3,877,013**
- Cleaned swap events output count: **3,877,013**
- Raw riders input count: **20,000**
- Cleaned riders output count: **20,000**
- Net record loss: **0 records (0.00%)**

All analytical subsets and exclusion rules are applied downstream dynamically using validity flags.