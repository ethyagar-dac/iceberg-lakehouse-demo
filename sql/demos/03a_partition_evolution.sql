-- Before: partitioned by month.
SHOW CREATE TABLE iceberg.nyc.yellow_trips;

-- Change the spec to daily. Metadata-only: no data files are touched.
ALTER TABLE iceberg.nyc.yellow_trips SET PROPERTIES partitioning = ARRAY['day(pickup_ts)'];

-- After: partitioned by day.
SHOW CREATE TABLE iceberg.nyc.yellow_trips;