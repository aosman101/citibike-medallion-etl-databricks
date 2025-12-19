from __future__ import annotations
import os
import psycopg2
from psycopg2.extras import execute_values

def conn():
    return psycopg2.connect(
        host=os.getenv("WAREHOUSE_HOST"),
        port=int(os.getenv("WAREHOUSE_PORT", "5432")),
        dbname=os.getenv("WAREHOUSE_DB"),
        user=os.getenv("WAREHOUSE_USER"),
        password=os.getenv("WAREHOUSE_PASSWORD"),
    )

def upsert_air_quality(rows: list[dict]) -> int:
    """
    Upserts flattened records into raw.air_quality_hourly.
    We use ON CONFLICT to make runs idempotent.
    """
    if not rows:
        return 0
    sql = """
      INSERT INTO raw.air_quality_hourly
      (sensor_id, location_id, location_name, parameter, units, latitude, longitude, ts_utc, value)
      VALUES %s
      ON CONFLICT (sensor_id, ts_utc)
      DO UPDATE SET value = EXCLUDED.value;
    """
    values = [
        (
            r["sensor_id"], r.get("location_id"), r.get("location_name"),
            r["parameter"], r.get("units"), r.get("latitude"), r.get("longitude"),
            r["ts_utc"], r.get("value"),
        )
        for r in rows
    ]
    with conn() as c, c.cursor() as cur:
        execute_values(cur, sql, values, page_size=1000)
    return len(values)
