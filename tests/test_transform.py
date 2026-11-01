from datetime import datetime

import pyarrow as pa

from taxi.transform import filter_to_month, month_bounds, rename_columns


def test_month_bounds_handles_december():
    assert month_bounds("2024-12") == (datetime(2024, 12, 1), datetime(2025, 1, 1))


def test_rename_columns():
    tt = pa.table({"VendorID": [1], "Airport_fee": [1.75]})
    assert rename_columns(tt).column_names == ["vendor_id", "airport_fee"]


def test_filter_to_month_drops_stray_rows():
    tt = pa.table(
        {
            "pickup_ts": [
                datetime(2024, 11, 15, 8, 30),  # inside November: kept
                datetime(2024, 10, 31, 23, 59),  # day before: dropped
                datetime(2008, 12, 31, 12, 0),  # stray old year: dropped
            ]
        }
    )
    assert filter_to_month(tt, "2024-11").num_rows == 1


def test_filter_to_month_boundaries():
    tt = pa.table(
        {"pickup_ts": [datetime(2024, 11, 1, 0, 0), datetime(2024, 12, 1, 0, 0)]}
    )
    assert (
        filter_to_month(tt, "2024-11").num_rows == 1
    )  # start is kept, end is excluded
