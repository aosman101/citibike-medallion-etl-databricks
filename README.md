# Citi Bike Medallion ETL (CSV → Delta) on Databricks

Hands-on data engineering showcase: ingest Citi Bike trip CSVs into a Databricks lakehouse, layer them through the Medallion pattern (Bronze → Silver → Gold), and surface Delta tables ready for analytics.

**Quick links:** [Badges](#badges) • [Why this project](#why-this-project) • [Architecture](#architecture-medallion) • [Dataset](#dataset-citi-bike-trip-histories-csv) • [Project layout](#project-layout) • [Run it](#quickstart-end-to-end) • [Outputs](#outputs-tables)


## Badges
[![Platform: Databricks](https://img.shields.io/badge/Platform-Databricks-EF2D5E?logo=databricks&logoColor=white)](https://www.databricks.com/)
[![Format: Delta Lake](https://img.shields.io/badge/Format-Delta%20Lake-0A7DBC)](https://delta.io/)
[![Architecture: Medallion](https://img.shields.io/badge/Architecture-Medallion-4E6E81)](#architecture-medallion)
[![Language: Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Workflow: Notebooks](https://img.shields.io/badge/Workflow-Databricks%20Notebooks-F47C20?logo=jupyter&logoColor=white)](#project-layout)


## Why this project
- Demonstrates job-ready lakehouse skills: CSV batch ingestion, Medallion layering, Delta tables, and basic DQ with quarantine.
- Parameterised month-by-month runs to keep compute/storage small while still realistic.
- Friendly to demos: end-to-end completes with one month of data on a small Databricks cluster.
- Extendable: add scheduling (Jobs), performance tuning (OPTIMIZE/ZORDER), or richer checks.


## Architecture (Medallion)
Bronze: land raw CSV rows + file metadata into Delta.  
Silver: apply schema, type casting, validation, deduplication, and quarantine invalid rows.  
Gold: aggregate for analytics (daily ridership, top stations, DQ summary).

Flow: CSVs → Bronze table → Silver table (+ invalid) → Gold tables.


## Dataset: Citi Bike Trip Histories (CSV)
- System data page: https://citibikenyc.com/system-data
- Bucket index (direct links): https://s3.amazonaws.com/tripdata/index.html
- Starter month (fast + budget-friendly): https://s3.amazonaws.com/tripdata/202401-citibike-tripdata.csv.zip

Tip: If your workspace blocks outbound internet, download locally and upload to DBFS or a Unity Catalog volume.


## Getting the CSVs into Databricks
**Option A (reliable): download locally, then upload**  
1) Download a monthly `.zip`.  
2) In Databricks: **New → Data → Upload**, store in DBFS/Volume.  
3) Unzip (patterns in `notebooks/01_download_and_ingest_bronze.py`).

**Option B (fastest if internet allowed): download from the notebook**  
Run `01_download_and_ingest_bronze.py` with `download_mode="auto_download"` to fetch, unzip, and copy into your configured folder automatically.


## Project layout
```
.
├── notebooks/
│   ├── 00_setup.py                  # Configure catalogs/schemas, base paths, widgets
│   ├── 01_download_and_ingest_bronze.py
│   ├── 02_transform_silver.py
│   └── 03_build_gold.py
├── docs/
│   └── data_dictionary.md           # Optional: column meanings and assumptions
└── README.md
```


## Quickstart (end-to-end)
1) Spin up a small Databricks cluster (single node is fine).  
2) Open `notebooks/00_setup.py` → run all cells (creates schemas + config widgets).  
3) Open `notebooks/01_download_and_ingest_bronze.py` → set `yyyymm` (e.g., `202401`) and run.  
4) Open `notebooks/02_transform_silver.py` → run for the same `yyyymm`.  
5) Open `notebooks/03_build_gold.py` → run to materialise analytics tables.  
6) Validate in Databricks SQL: query Gold tables to spot-check counts and top stations.


## Outputs (tables)
- Bronze: `{prefix}_bronze.citibike_trips_bronze`
- Silver: `{prefix}_silver.citibike_trips_silver`
- Silver quarantine: `{prefix}_silver.citibike_trips_invalid`
- Gold: `{prefix}_gold.citibike_daily_ridership`, `{prefix}_gold.citibike_top_start_stations`, etc.
- Gold DQ summary: `{prefix}_gold.citibike_dq_summary`


## Next improvements (pick and try)
- Add OPTIMIZE/ZORDER for faster queries after initial loads.
- Persist basic DQ metrics (row counts, null thresholds) and alert on drift.
- Orchestrate with a Databricks Jobs workflow (00 → 01 → 02 → 03 nightly/weekly).
- Layer in unit tests for transformations or add expectations via Delta Live Tables.


## References
- Medallion Architecture (Databricks): https://docs.databricks.com/aws/en/lakehouse/medallion
- Upload files to Databricks: https://docs.databricks.com/aws/en/ingestion/file-upload/
- Download data from the internet: https://docs.databricks.com/aws/en/ingestion/file-upload/download-internet-files
- Expand/unzip zip files: https://docs.databricks.com/aws/en/files/unzip-files
- Delta Lake tutorial: https://docs.databricks.com/aws/en/delta/tutorial
