# Databricks notebook source
# COMMAND ----------
# MAGIC %md
# MAGIC # 00 - Setup
# MAGIC Creates Bronze/Silver/Gold schemas and config used by the pipeline.

# COMMAND ----------
from pyspark.sql import functions as F

# ----- Widgets (edit defaults if you want) -----
dbutils.widgets.text("catalog", "main", "Unity Catalog catalog (if enabled)")
dbutils.widgets.text("schema_prefix", "citibike_medallion", "Prefix for schemas/databases")
dbutils.widgets.text("storage_base", "dbfs:/FileStore/citibike_medallion", "Base path for raw files & checkpoints")
dbutils.widgets.text("use_unity_catalog", "", "Optional: true/false (blank=auto)")


def _to_bool(s: str):
    if s is None:
        return None
    s = s.strip().lower()
    if s in ("true", "1", "yes", "y"):
        return True
    if s in ("false", "0", "no", "n"):
        return False
    return None


CATALOG = dbutils.widgets.get("catalog").strip()
PREFIX = dbutils.widgets.get("schema_prefix").strip()
STORAGE_BASE = dbutils.widgets.get("storage_base").rstrip("/")
forced_uc = _to_bool(dbutils.widgets.get("use_unity_catalog"))


def supports_unity_catalog() -> bool:
    """
    If your workspace supports Unity Catalog, SHOW CATALOGS should work.
    If not, we fall back to the legacy Hive metastore approach.
    """
    if forced_uc is not None:
        return forced_uc
    try:
        spark.sql("SHOW CATALOGS").limit(1).collect()
        return True
    except Exception:
        return False


USE_UC = supports_unity_catalog()

BRONZE_SCHEMA = f"{PREFIX}_bronze"
SILVER_SCHEMA = f"{PREFIX}_silver"
GOLD_SCHEMA = f"{PREFIX}_gold"


def fqtn(schema: str, table: str) -> str:
    """Fully-qualified table name for either UC or legacy metastore."""
    return f"{CATALOG}.{schema}.{table}" if USE_UC else f"{schema}.{table}"


# ----- Create schemas/databases -----
if USE_UC:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{BRONZE_SCHEMA}")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SILVER_SCHEMA}")
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{GOLD_SCHEMA}")
else:
    # Legacy metastore uses CREATE DATABASE / CREATE SCHEMA interchangeably
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {BRONZE_SCHEMA}")
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {SILVER_SCHEMA}")
    spark.sql(f"CREATE DATABASE IF NOT EXISTS {GOLD_SCHEMA}")


# ----- Non-tabular storage locations (raw files, logs) -----
RAW_BASE = f"{STORAGE_BASE}/raw"
BAD_RECORDS_BASE = f"{STORAGE_BASE}/bad_records"
CHECKPOINT_BASE = f"{STORAGE_BASE}/checkpoints"

for p in [RAW_BASE, BAD_RECORDS_BASE, CHECKPOINT_BASE]:
    dbutils.fs.mkdirs(p)


# ----- Persist config for other notebooks on this cluster -----
spark.conf.set("citibike_medallion.use_uc", str(USE_UC).lower())
spark.conf.set("citibike_medallion.catalog", CATALOG)
spark.conf.set("citibike_medallion.bronze_schema", BRONZE_SCHEMA)
spark.conf.set("citibike_medallion.silver_schema", SILVER_SCHEMA)
spark.conf.set("citibike_medallion.gold_schema", GOLD_SCHEMA)
spark.conf.set("citibike_medallion.storage_base", STORAGE_BASE)
spark.conf.set("citibike_medallion.raw_base", RAW_BASE)
spark.conf.set("citibike_medallion.bad_records_base", BAD_RECORDS_BASE)
spark.conf.set("citibike_medallion.checkpoint_base", CHECKPOINT_BASE)

display(
    spark.createDataFrame(
        [
            {
                "USE_UC": USE_UC,
                "CATALOG": CATALOG,
                "BRONZE_SCHEMA": BRONZE_SCHEMA,
                "SILVER_SCHEMA": SILVER_SCHEMA,
                "GOLD_SCHEMA": GOLD_SCHEMA,
                "RAW_BASE": RAW_BASE,
                "STORAGE_BASE": STORAGE_BASE,
            }
        ]
    )
)
