"""Load one month from s3://raw into the Iceberg table, replacing that month."""

import os
import sys

import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow import fs
from pyiceberg.expressions import And, GreaterThanOrEqual, LessThan
from pyiceberg.table import Table
from pyiceberg.transforms import MonthTransform

from taxi.config import NAMESPACE, RAW_BUCKET, TABLE, get_catalog, load_env
from taxi.download import raw_key
from taxi.transform import month_bounds, transform


def read_raw(month: str) -> pa.Table:
    """Read the month's raw Parquet file from MinIO into a pyarrow Table."""
    s3fs = fs.S3FileSystem(
        endpoint_override=os.environ["S3_ENDPOINT"].removeprefix("http://"),
        scheme="http",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    )
    return pq.read_table(f"{RAW_BUCKET}/{raw_key(month)}", filesystem=s3fs)


def get_or_create_table(catalog, schema: pa.Schema) -> Table:
    """Load the table, or create it on first run, partitioned by month(pickup_ts)."""
    catalog.create_namespace_if_not_exists(NAMESPACE)
    if catalog.table_exists(TABLE):
        return catalog.load_table(TABLE)

    table = catalog.create_table(TABLE, schema=schema)
    # Partition spec: one partition per month of pickup time.
    table.update_spec().add_field(
        "pickup_ts", MonthTransform(), "pickup_month"
    ).commit()
    print(f"created {TABLE}, partitioned by month(pickup_ts)")
    return table


def month_filter(month: str):
    """Iceberg row filter: start <= pickup_ts < end."""
    start, end = month_bounds(month)
    return And(
        GreaterThanOrEqual("pickup_ts", start.isoformat()),
        LessThan("pickup_ts", end.isoformat()),
    )


def load(month: str) -> None:
    load_env()
    df = transform(read_raw(month), month)
    print(f"{month}: {df.num_rows} rows after transform")

    catalog = get_catalog()
    table = get_or_create_table(catalog, df.schema)

    # Schema evolution: add any new source columns (e.g. cbd_congestion_fee in 2025-01).
    # Metadata-only change; existing files are not rewritten. No-op if nothing is new.
    with table.update_schema() as update:
        update.union_by_name(df.schema)

    # Idempotent write: delete this month's rows and add the new ones in ONE commit.
    table.overwrite(df, overwrite_filter=month_filter(month))
    print(
        f"{month}: written to {TABLE} (snapshot {table.current_snapshot().snapshot_id})"
    )


if __name__ == "__main__":
    load(sys.argv[1])  # usage: python -m taxi.load 2024-11
