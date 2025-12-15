# Citi Bike Medallion ETL (CSV → Delta) on Databricks

A portfolio-ready **data engineering** project that implements the **Medallion Architecture (Bronze → Silver → Gold)** in **Databricks** using **CSV trip history files** from **NYC Citi Bike** and storing curated outputs as **Delta Lake tables**.

## Why this project?
This repo demonstrates practical, job-relevant skills:
- Batch ingestion from CSV into a lakehouse.
- Medallion layering (raw → validated → analytics-ready).
- Basic data quality checks + quarantine of invalid records.
- Delta Lake tables (reliable storage + table history).
- Parameterised runs (e.g., ingest one month at a time).
- Optional scheduling via Databricks Jobs.

## Architecture (Medallion)
CSV (raw files)
   |
   v
BRONZE  (raw-as-is + metadata)        -> Delta table
   |
   v
SILVER  (typed, validated, deduped)   -> Delta table + invalid/quarantine table
   |
   v
GOLD    (aggregations for analytics)  -> Delta tables (daily usage, top stations, etc.)

## Dataset: Citi Bike Trip Histories (CSV)
Citi Bike publishes downloadable trip history files (compressed CSVs) here:
- Citi Bike System Data page: https://citibikenyc.com/system-data
- “Download Citi Bike trip history data” bucket index: https://s3.amazonaws.com/tripdata/index.html

### Recommended small-scope approach (fast + budget-friendly)
Pick **one month** to start (example below uses Jan 2024):
- https://s3.amazonaws.com/tripdata/202401-citibike-tripdata.csv.zip

> Note: Some environments block outbound internet access from clusters. If so, download locally and upload to Databricks instead.

## Getting the CSVs into Databricks (2 options)

### Option A — Download locally, then upload to Databricks (most reliable)
1. Download a monthly `.zip` from the links above.
2. In Databricks: **New → Data** and use file upload to store the file (DBFS or a Unity Catalogue Volume).
3. Unzip it (see `01_download_and_ingest_bronze.py` for code patterns).

### Option B — Download directly from a notebook (fastest if internet is allowed)
Run the ingestion notebook with `download_mode=auto_download` and it will:
- Download the zip to the driver's ephemeral storage
- unzip it
- copy CSVs into your configured DBFS folder

## Project structure
.
├── notebooks/
│   ├── 00_setup.py
│   ├── 01_download_and_ingest_bronze.py
│   ├── 02_transform_silver.py
│   └── 03_build_gold.py
├── docs/
│   └── data_dictionary.md              # (optional) explain columns + assumptions
├── .gitignore
└── README.md

## Quickstart (end-to-end)
1. Create a Databricks cluster (small / single-node is fine).
2. Run `notebooks/00_setup.py` to create schemas + set config.
3. Run `notebooks/01_download_and_ingest_bronze.py` for a month (e.g., `yyyymm=202401`).
4. Run `notebooks/02_transform_silver.py` for the same month.
5. Run `notebooks/03_build_gold.py` to generate analytics tables.
6. Query Gold tables in Databricks SQL to validate results.

## Outputs (tables)
- Bronze: `{prefix}_bronze.citibike_trips_bronze`
- Silver: `{prefix}_silver.citibike_trips_silver`
- Silver quarantine: `{prefix}_silver.citibike_trips_invalid`
- Gold: `{prefix}_gold.citibike_daily_ridership`, `{prefix}_gold.citibike_top_start_stations`, etc.
- Gold DQ summary: `{prefix}_gold.citibike_dq_summary`

## Next improvements (optional)
- Add OPTIMIZE / ZORDER for performance
- Add unit-like checks (row counts, null thresholds) and persist metrics
- Add a Jobs workflow (3 notebook tasks) to run nightly/weekly

## References
- Medallion Architecture (Databricks): https://docs.databricks.com/aws/en/lakehouse/medallion
- Upload files to Databricks: https://docs.databricks.com/aws/en/ingestion/file-upload/
- Download data from the internet: https://docs.databricks.com/aws/en/ingestion/file-upload/download-internet-files
- Expand/unzip zip files: https://docs.databricks.com/aws/en/files/unzip-files
- Delta Lake tutorial: https://docs.databricks.com/aws/en/delta/tutorial
