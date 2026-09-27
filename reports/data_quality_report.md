# VoltRelay Energy: Comprehensive Data Quality & Integrity Audit Report

**Date of Audit**: 2026-09-27  
**Lead Roles**: Lead Data Analyst, Analytics Engineer, BI Architect  
**Status**: Pre-cleaning audit complete (Read-only verification)  

---

## 1. Executive Summary & Inventory Match

A rigorous, read-only quality inspection was performed across all 8 relational tables for the VoltRelay battery-swapping network.
Actual record counts were compared against expectations from the Hackathon Problem Statement:

| dataset               |   rows_actual |   rows_expected |   rows_diff |   columns |   duplicate_rows | pk_columns            | pk_unique   |   pk_duplicates |   total_null_cells |   total_null_pct |
|:----------------------|--------------:|----------------:|------------:|----------:|-----------------:|:----------------------|:------------|----------------:|-------------------:|-----------------:|
| swap_events           |       3877013 |         3877013 |           0 |        22 |                0 | event_id              | True        |               0 |            1037944 |             1.22 |
| station_hourly_status |       1487712 |         1487712 |           0 |        14 |                0 | station_id+hour_start | True        |               0 |             896880 |             4.31 |
| riders                |         20000 |           20000 |           0 |        12 |                0 | rider_id              | True        |               0 |              12837 |             5.35 |
| batteries             |          6500 |            6500 |           0 |        13 |                0 | battery_id            | True        |               0 |              10124 |            11.98 |
| support_tickets       |         44000 |           44000 |           0 |        12 |                0 | ticket_id             | True        |               0 |              50445 |             9.55 |
| stations              |           152 |             152 |           0 |        22 |                0 | station_id            | True        |               0 |                293 |             8.76 |
| city_daily_context    |          3282 |            3282 |           0 |        12 |                0 | city+date             | True        |               0 |               3172 |             8.05 |
| fleet_partners        |            12 |              12 |           0 |        12 |                0 | partner_id            | True        |               0 |                 22 |            15.28 |

> [!NOTE]
> **Row Count Concordance**: All 8 datasets match the documented row counts with **100% exact parity** (0 row divergence across 5.4M+ combined rows).

---

## 2. Key Integrity Audit (Primary & Foreign Keys)

| source_dataset        | key_type   | source_column(s)      | target_dataset   | target_column   | is_optional   |   violation_count |   violation_pct | status   |
|:----------------------|:-----------|:----------------------|:-----------------|:----------------|:--------------|------------------:|----------------:|:---------|
| swap_events           | PRIMARY    | event_id              | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| station_hourly_status | PRIMARY    | station_id+hour_start | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| riders                | PRIMARY    | rider_id              | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| batteries             | PRIMARY    | battery_id            | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| support_tickets       | PRIMARY    | ticket_id             | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| stations              | PRIMARY    | station_id            | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| city_daily_context    | PRIMARY    | city+date             | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| fleet_partners        | PRIMARY    | partner_id            | N/A              | N/A             | False         |                 0 |               0 | PASS     |
| swap_events           | FOREIGN    | rider_id              | riders           | rider_id        | False         |                 0 |               0 | PASS     |
| swap_events           | FOREIGN    | station_id            | stations         | station_id      | False         |                 0 |               0 | PASS     |
| swap_events           | FOREIGN    | battery_in_id         | batteries        | battery_id      | True          |                 0 |               0 | PASS     |
| swap_events           | FOREIGN    | battery_out_id        | batteries        | battery_id      | True          |                 0 |               0 | PASS     |
| riders                | FOREIGN    | partner_id            | fleet_partners   | partner_id      | True          |                 0 |               0 | PASS     |
| station_hourly_status | FOREIGN    | station_id            | stations         | station_id      | False         |                 0 |               0 | PASS     |
| support_tickets       | FOREIGN    | rider_id              | riders           | rider_id        | False         |                 0 |               0 | PASS     |
| support_tickets       | FOREIGN    | station_id            | stations         | station_id      | True          |                 0 |               0 | PASS     |
| support_tickets       | FOREIGN    | battery_id            | batteries        | battery_id      | True          |                 0 |               0 | PASS     |

### Key Integrity Findings:
- **Primary Keys**: Every dataset's documented primary key is 100% unique. There are **0 duplicate primary key records**.
- **Foreign Keys**: All core foreign keys (`swap_events.rider_id -> riders`, `swap_events.station_id -> stations`, `station_hourly_status.station_id -> stations`, `support_tickets.rider_id -> riders`) show **100% referential integrity** (0 orphaned records).
- **Optional Foreign Keys**: In `swap_events`, `battery_out_id` is null during failed swaps (as expected when no battery was dispensed), while `battery_in_id` matches the battery fleet.

---

## 3. Investigation of Known Domain Issues

### 3.1 Swap Event Types & Failure Proportions
- **Completed Swaps**: 94.037% of total swap attempts.
- **Failed / Incomplete Swaps**: 5.963% of total swap attempts.
- **Detailed Breakdown by Attempt Outcome**:
  - `swap_completed`: **3,645,809** (94.04%)
  - `failed_no_charged_battery`: **134,389** (3.47%)
  - `abandoned_queue`: **68,533** (1.77%)
  - `cancelled_by_rider`: **16,712** (0.43%)
  - `failed_system_error`: **11,570** (0.30%)

### 3.2 Firmware v3.2.0 Timestamp Glitch (5h 30m Offset)
- **Total Swaps logged under Firmware v3.2.0**: 1,561,174
- **v3.2.0 Swaps in Bug Window (2025-03-10 to 2025-04-14)**: **135,601**
- **Impact**: Timestamps logged by stations on firmware v3.2.0 during this window are recorded ~5 hours and 30 minutes earlier than true local time (UTC vs IST drift).
- **Cleaning Action**: Create `original_event_ts`, `corrected_event_ts`, and `timestamp_corrected_flag` during the cleaning stage. Never overwrite raw timestamps in-place.

### 3.3 Rider `home_city` Spelling Inconsistencies
- Unique spellings discovered in `riders.home_city`:
  - `Bengaluru`: 4,175 riders
  - `Delhi NCR`: 3,783 riders
  - `Hyderabad`: 3,396 riders
  - `Pune`: 2,843 riders
  - `Mumbai`: 2,772 riders
  - `Jaipur`: 2,446 riders
  - `Bombay`: 53 riders
  - `BLR`: 53 riders
  - `bengaluru `: 50 riders
  - `MUM`: 49 riders
  - `pune`: 43 riders
  - `PUN`: 43 riders
  - `New Delhi`: 42 riders
  - `JAI`: 41 riders
  - `Gurgaon`: 36 riders
  - `Bangalore`: 32 riders
  - `HYD`: 31 riders
  - `Hyd`: 31 riders
  - `jaipur`: 29 riders
  - `hyderabad`: 27 riders
  - `Delhi`: 25 riders
- **Stations City Distribution** (canonical reference):
  - `Bengaluru`: 34 stations
  - `Delhi NCR`: 30 stations
  - `Hyderabad`: 26 stations
  - `Pune`: 22 stations
  - `Mumbai`: 22 stations
  - `Jaipur`: 18 stations
- **Cleaning Action**: Build a dictionary mapping variations (e.g. Bangalore/BLR -> Bengaluru) to standard canonical cities while preserving the raw column.

### 3.4 Connectivity & Near-Duplicate Swaps
- **Offline Batch Events**: 591,114 (591114 total)
- **Exact Rider + Timestamp Duplicates**: 34
- **Exact Rider + Station + Timestamp Duplicates**: 26
- **Analytical Decision**: Flag suspicious near-duplicates resulting from packet re-transmissions; do NOT blindly drop records without assessing attempt sequences and financial reconciliation.

### 3.5 Odometer & Distance Anomalies (`km_since_last_swap`)
- **Negative Distance (< 0 km)**: 7,814 records
- **Zero Distance (0 km)**: 0 records (often immediate retry after swap failure)
- **Implausibly High (> 500 km)**: 0 records
- **Extreme Outliers (> 1,000 km)**: 0 records
- **Range**: Min = -20.0 km, Max = 420.0 km, Median = 60.0 km
- **Cleaning Action**: Create `valid_km_flag`. Exclude invalid odometer readings when analyzing battery consumption and range per swap.

### 3.6 Battery Telemetry Outliers: SOC & SOH > 100%
- **Swap Events SOC / SOH Checks**:
  - `soc_in_pct`: Over 100% = **0**, Under 0% = 0, Max = 28.4, Nulls = 28,282
  - `soh_in_pct`: Over 100% = **3,356**, Under 0% = 0, Max = 101.4, Nulls = 28,282
  - `soc_out_pct`: Over 100% = **3,698**, Under 0% = 0, Max = 103.0, Nulls = 231,204
  - `soh_out_pct`: Over 100% = **2,799**, Under 0% = 0, Max = 101.3, Nulls = 231,204
- **Batteries Master SOH Checks**:
  - `initial_soh_pct`: Over 100% = **0**, Under 0% = 0, Max = 100.0, Nulls = 0
  - `current_soh_pct`: Over 100% = **0**, Under 0% = 0, Max = 88.6, Nulls = 0
- **Treatment**: Sensor calibration calibration artifacts (> 100% up to ~105%) must be clipped or flagged with `soc_valid_flag` and `soh_valid_flag`.

### 3.7 Station Telemetry Missingness
- **Station Hourly Records**: 1,487,712
- **Telemetry Status Distribution**:
  - `ok`: 1,441,341
  - `partial`: 36,987
  - `missing`: 9,384
- **Metric Null Counts when Telemetry Down**:
  - `ambient_temp_c`: 9,384 missing values
  - `cabinet_temp_c`: 9,384 missing values
  - `grid_kwh`: 9,384 missing values
  - `charged_2w_avg`: 9,384 missing values
> [!IMPORTANT]
> **Rule Compliance**: Missing telemetry fields are strictly **preserved as nulls** rather than imputed as 0, preventing severe distortion of temperature, power, and availability averages.

### 3.8 Support Tickets & Non-Random CSAT Missingness
- **Total Support Tickets**: 44,000
- **CSAT Missing Responses**: 28,871 (65.62% unrated)
- **CSAT Response Rate**: 34.38%
- **Average Rating (1-5 scale)**: 3.56
- **Resolution Statuses**:
  - `resolved`: 37,888
  - `unresolved`: 5,175
  - `duplicate`: 937
- **Finding**: Unhappy or unresolved riders disproportionately submit tickets or drop off without rating. CSAT missingness is non-random (informative missingness).

### 3.9 Test Stations (`STN-TST`)
- **Identified Test Stations**: ['STN-TST-01', 'STN-TST-02']
- **Swaps Recorded at Test Stations**: 62,031 transactions
- **Revenue from Test Stations**: ₹3,930,760.05
- **Analytical Treatment**: Filter out test station activity from commercial operational KPIs, SLA compliance, and financial margin figures.

---

## 4. Column Missingness Summary

### swap_events (Columns with Missing Values)
- `battery_in_id`: 28,282 nulls (0.73%)
- `battery_out_id`: 231,204 nulls (5.96%)
- `soc_in_pct`: 28,282 nulls (0.73%)
- `soh_in_pct`: 28,282 nulls (0.73%)
- `soc_out_pct`: 231,204 nulls (5.96%)
- `soh_out_pct`: 231,204 nulls (5.96%)
- `km_since_last_swap`: 28,282 nulls (0.73%)
- `energy_to_recharge_kwh`: 231,204 nulls (5.96%)

### station_hourly_status (Columns with Missing Values)
- `charged_2w_avg`: 9,384 nulls (0.63%)
- `charged_2w_min`: 9,384 nulls (0.63%)
- `charged_3w_min`: 821,808 nulls (55.24%)
- `packs_charging`: 9,384 nulls (0.63%)
- `packs_quarantined`: 9,384 nulls (0.63%)
- `ambient_temp_c`: 9,384 nulls (0.63%)
- `cabinet_temp_c`: 9,384 nulls (0.63%)
- `avg_charge_minutes`: 9,384 nulls (0.63%)
- `grid_kwh`: 9,384 nulls (0.63%)

### riders (Columns with Missing Values)
- `partner_id`: 7,628 nulls (38.14%)
- `declared_shift`: 3,662 nulls (18.31%)
- `age_band`: 1,547 nulls (7.74%)

### batteries (Columns with Missing Values)
- `retired_date`: 5,062 nulls (77.88%)
- `retirement_reason`: 5,062 nulls (77.88%)

### support_tickets (Columns with Missing Values)
- `station_id`: 2,227 nulls (5.06%)
- `battery_id`: 13,235 nulls (30.08%)
- `resolution_hours`: 6,112 nulls (13.89%)
- `csat_score`: 28,871 nulls (65.62%)

### stations (Columns with Missing Values)
- `decommissioned_date`: 151 nulls (99.34%)
- `competitor_within_1_5km_since`: 142 nulls (93.42%)

### city_daily_context (Columns with Missing Values)
- `festival_or_event`: 3,172 nulls (96.65%)

### fleet_partners (Columns with Missing Values)
- `amendment_date`: 11 nulls (91.67%)
- `discount_pct_after_amendment`: 11 nulls (91.67%)

---

## 5. Summary of Audit Recommendations for Cleaning Layer

| Issue | Affected Dataset(s) | Detection Condition | Cleaning Action |
|:------|:--------------------|:--------------------|:----------------|
| Firmware Timestamp Glitch | `swap_events` | `station_firmware == 'v3.2.0'` & date between Mar 10 and Apr 14, 2025 | Add +5.5 hours to `corrected_event_ts`; create `timestamp_corrected_flag` |
| City Name Variants | `riders` | Variant spellings in `home_city` | Standardize to canonical city in `clean_home_city`; preserve `home_city` |
| Offline Duplicate Swaps | `swap_events` | Multiple events same rider + station + ts | Create `near_duplicate_flag` |
| Invalid Odometer | `swap_events` | `km_since_last_swap < 0` or `> 500` | Create `valid_km_flag`; do not delete raw value |
| Out-of-bounds SOC / SOH | `swap_events`, `batteries` | Values > 100% or < 0% | Create `valid_soc_flag`, `valid_soh_flag`; clip or isolate |
| Missing Telemetry | `station_hourly_status` | `telemetry_status != 'online'` | Retain as `NaN` (do not impute 0) |
| Test Station Transactions | `swap_events`, `stations` | `station_id` starts with `STN-TST` | Create `is_test_station_flag`; filter from production KPIs |
| CSAT Non-response | `support_tickets` | `csat_score.isna()` | Preserve as missing; analyze response bias |

**Conclusion**: The datasets are structurally integral with complete primary/foreign key coherence. Systematic flags will now be applied in `src/data_cleaning.py` to ensure reproducible, auditable analytics without data loss.