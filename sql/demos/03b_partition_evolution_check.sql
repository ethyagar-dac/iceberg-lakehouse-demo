-- Two layouts in ONE table: spec 0 = monthly (Nov, Jan), spec 1 = daily (Dec, ~31 files).
SELECT spec_id, count(*) AS files, sum(record_count) AS rows
FROM iceberg.nyc."yellow_trips$files"
GROUP BY spec_id ORDER BY spec_id;

-- Queries don't care: same SQL across both layouts, and the totals are unchanged.
SELECT date_trunc('month', pickup_ts) AS month, count(*) AS trips
FROM iceberg.nyc.yellow_trips GROUP BY 1 ORDER BY 1;

-- Pruning: one day in December (daily spec) reads a single small file...
EXPLAIN ANALYZE SELECT count(*) FROM iceberg.nyc.yellow_trips
WHERE pickup_ts >= TIMESTAMP '2024-12-10 00:00:00' AND pickup_ts < TIMESTAMP '2024-12-11 00:00:00';

-- ...one day in November (monthly spec) has to open the whole month's file.
EXPLAIN ANALYZE SELECT count(*) FROM iceberg.nyc.yellow_trips
WHERE pickup_ts >= TIMESTAMP '2024-11-10 00:00:00' AND pickup_ts < TIMESTAMP '2024-11-11 00:00:00';