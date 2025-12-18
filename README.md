# London Air Quality + Weather Lakehouse (Airflow • dbt • Postgres • MinIO • Metabase)

Local-first, 100% free/open-source data platform:
- Ingest air-quality data (OpenAQ) + weather data (Open‑Meteo)
- Land raw payloads in an S3-compatible data lake (MinIO)
- Load and model analytics tables in Postgres using dbt (incremental)
- Validate with Great Expectations
- Explore in Metabase dashboards

Note: This repository is designed as a learning and portfolio project. Airflow’s Docker Compose setup provides a quick-start environment (not suitable for production).  
> See Airflow docs for caveats. https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html

---

## Architecture

      +------------------+          +-------------------+
      |   OpenAQ API      |          |   Open-Meteo API   |
      +---------+---------+          +---------+---------+
                |                              |
                v                              v
         +------+-------------------------------+------+
         |                Apache Airflow               |
         |  DAG: extract -> land -> load -> transform  |
         +------+-------------------------------+------+
                |                              |
                v                              v
      +------------------+          +-------------------+
      |  MinIO (S3 lake) |          | Postgres (warehouse)|
      | raw JSON objects |          | raw/stg/marts tables|
      +---------+--------+          +---------+----------+
                |                              |
                +---------------+--------------+
                                v
                           +----+----+
                           | Metabase|
                           +---------+



---

## Tech stack

- **Orchestration:** Apache Airflow (TaskFlow API)
- **Lake storage:** MinIO (S3-compatible)
- **Warehouse:** Postgres
- **Transform:** dbt Core (incremental models)
- **Data quality:** Great Expectations (checkpoints)
- **BI:** Metabase

References:
- Airflow TaskFlow API tutorial: https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html
- OpenAQ API docs: https://docs.openaq.org/
- Open‑Meteo docs (no API key required): https://open-meteo.com/en/docs
- MinIO S3 compatibility: https://www.min.io/product/aistor/s3-compatibility
- Metabase on Docker: https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker

---

## Quickstart (local)

### Prerequisites
- Docker + Docker Compose
- A free OpenAQ API key (store as env var `OPENAQ_API_KEY`)

### 1) Configure environment
Copy `.env.example` to `.env` and fill in values:
- `OPENAQ_API_KEY=...`
- `MINIO_ROOT_USER=...`
- `MINIO_ROOT_PASSWORD=...`
- `WAREHOUSE_PASSWORD=...`

### 2) Start services
```bash
docker compose -f docker/compose.yaml up -d --build
