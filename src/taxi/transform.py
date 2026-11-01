"""Pure transformations on one month of TLC yellow taxi data (pyarrow tables)."""

from datetime import datetime

import pyarrow as pa
import pyarrow.compute as pc

# Source name -> our name. Columns not listed are just lowercased.
RENAMES = {
    "VendorID": "vendor_id",
    "tpep_pickup_datetime": "pickup_ts",
    "tpep_dropoff_datetime": "dropoff_ts",
    "RatecodeID": "rate_code_id",
    "PULocationID": "pickup_location_id",
    "DOLocationID": "dropoff_location_id",
}


def rename_columns(table: pa.Table) -> pa.Table:
    """Apply RENAMES; lowercase any column not listed."""
    new_names = [RENAMES.get(name, name.lower()) for name in table.column_names]
    return table.rename_columns(new_names)


def month_bounds(month: str) -> tuple[datetime, datetime]:
    """'2024-11' -> (2024-11-01 00:00, 2024-12-01 00:00). End is exclusive."""
    start = datetime.strptime(month, "%Y-%m")
    if start.month == 12:
        end = datetime(start.year + 1, 1, 1)
    else:
        end = datetime(start.year, start.month + 1, 1)
    return start, end


def filter_to_month(table: pa.Table, month: str) -> pa.Table:
    """Keep rows with start <= pickup_ts < end."""
    start, end = month_bounds(month)
    col = table["pickup_ts"]
    mask = pc.and_(pc.greater_equal(col, start), pc.less(col, end))
    return table.filter(mask)


def transform(table: pa.Table, month: str) -> pa.Table:
    """Rename columns, then keep only rows inside the file's month."""
    renamed = rename_columns(table)
    return filter_to_month(renamed, month)
