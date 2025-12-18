-- TODO: bootstrap warehouse schemas/tables for the lakehouse project
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS marts;

-- Flattened hourly air-quality observations (one row per sensor-hour)
CREATE TABLE IF NOT EXISTS raw.air_quality_hourly (
  sensor_id      BIGINT NOT NULL,
  location_id    BIGINT NULL,
  location_name  TEXT NULL,
  parameter      TEXT NOT NULL,
  units          TEXT NULL,
  latitude       DOUBLE PRECISION NULL,
  longitude      DOUBLE PRECISION NULL,
  ts_utc         TIMESTAMPTZ NOT NULL,
  value          DOUBLE PRECISION NULL,
  ingested_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (sensor_id, ts_utc)
);

-- Hourly weather observations for a coordinate (one row per coord-hour)
CREATE TABLE IF NOT EXISTS raw.weather_hourly (
  latitude    DOUBLE PRECISION NOT NULL,
  longitude   DOUBLE PRECISION NOT NULL,
  ts_utc      TIMESTAMPTZ NOT NULL,
  temp_2m     DOUBLE PRECISION NULL,
  wind_10m    DOUBLE PRECISION NULL,
  precip_mm   DOUBLE PRECISION NULL,
  ingested_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (latitude, longitude, ts_utc)
);
