"""Load one month from s3://raw into the Iceberg table, replacing that month."""

import sys

import pyarrow as pa
import pyarrow.parquet as pq
from pyiceberg.expressions import And, GreaterThanOrEqual, LessThan
from pyiceberg.table import Table
from pyiceberg.transforms import MonthTransform

from taxi.config import NAMESPACE, RAW_BUCKET, TABLE, arrow_s3fs, get_catalog, load_env
from taxi.download import raw_key
from taxi.transform import month_bounds, transform


def read_raw(month: str) -> pa.Table:
    """Read the month's raw Parquet file from MinIO into a pyarrow Table."""
    return pq.read_table(f"{RAW_BUCKET}/{raw_key(month)}", filesystem=arrow_s3fs())


def get_or_create_table(catalog, schema: pa.Schema) -> Table:
    """Load the table, or create it on first run, partitioned by month(pickup_ts)."""
    catalog.create_namespace_if_not_exists(NAMESPACE)
    if catalog.table_exists(TABLE):
        return catalog.load_table(TABLE)

    table = catalog.create_table(TABLE, schema=schema)
    table.update_spec().add_field(
        "pickup_ts", MonthTransform(), "pickup_month"
    ).commit()
    print(f"created {TABLE}, partitioned by month(pickup_ts)")
    return table


def align_to_table(df: pa.Table, table: Table) -> pa.Table:
    """Match the table's columns: add NULL columns the month lacks, then use table order.

    Needed when an older month (no cbd_congestion_fee) is reloaded after a newer one.
    """
    target = table.schema().as_arrow()
    for field in target:
        if field.name not in df.column_names:
            df = df.append_column(field.name, pa.nulls(df.num_rows, type=field.type))
    return df.select(target.names)


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

    # Schema evolution: add new source columns to the table (metadata-only; no-op if none).
    with table.update_schema() as update:
        update.union_by_name(df.schema)

    # Older months lack newer columns: fill with NULL so the write matches the table.
    df = align_to_table(df, table)

    # Idempotent write: replace this month's rows in one atomic commit.
    table.overwrite(df, overwrite_filter=month_filter(month))
    print(
        f"{month}: written to {TABLE} (snapshot {table.current_snapshot().snapshot_id})"
    )


if __name__ == "__main__":
    load(sys.argv[1])  # usage: python -m taxi.load 2024-11
