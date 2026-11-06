"""Data quality checks for one loaded month, run as SQL in Trino."""

import os
import sys

import pyarrow.parquet as pq

import trino
from taxi.config import RAW_BUCKET, TABLE, arrow_s3fs, load_env
from taxi.download import raw_key
from taxi.transform import month_bounds

MIN_KEPT_RATIO = 0.99  # transform only drops stray-date rows; losing >1% means a bug


def raw_row_count(month: str) -> int:
    """Rows in the source file, read from the Parquet footer only (no data scan)."""
    path = f"{RAW_BUCKET}/{raw_key(month)}"
    return pq.ParquetFile(path, filesystem=arrow_s3fs()).metadata.num_rows


def loaded_row_count(month: str) -> int:
    """Rows in the Iceberg table for this month, counted by Trino."""
    start, end = month_bounds(month)
    conn = trino.dbapi.connect(
        host=os.environ["TRINO_HOST"],
        port=8080,
        user="pipeline",
        catalog="iceberg",
        schema="nyc",
    )
    cur = conn.cursor()
    cur.execute(
        f"SELECT count(*) FROM {TABLE} "
        f"WHERE pickup_ts >= TIMESTAMP '{start:%Y-%m-%d %H:%M:%S}' "
        f"AND pickup_ts < TIMESTAMP '{end:%Y-%m-%d %H:%M:%S}'"
    )
    return cur.fetchone()[0]


def check(month: str) -> None:
    """Raise ValueError if the month failed any check (fails the Airflow task)."""
    load_env()
    raw, loaded = raw_row_count(month), loaded_row_count(month)
    ratio = loaded / raw if raw else 0
    print(f"{month}: raw={raw} loaded={loaded} kept={ratio:.4%}")

    if loaded == 0:
        raise ValueError(f"{month}: no rows loaded")
    if loaded > raw:
        raise ValueError(f"{month}: more rows loaded than in source (duplicates?)")
    if ratio < MIN_KEPT_RATIO:
        raise ValueError(f"{month}: kept only {ratio:.2%} of source rows")
    print(f"{month}: quality checks passed")


if __name__ == "__main__":
    check(sys.argv[1])  # usage: python -m taxi.quality 2024-11
