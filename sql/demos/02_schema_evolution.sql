-- The column added by the 2025-01 load (union_by_name). No files were rewritten.
DESCRIBE iceberg.nyc.yellow_trips;

-- Older months return NULL for the new column; January is populated.
SELECT date_trunc('month', pickup_ts) AS month,
       count(*)                  AS trips,
       count(cbd_congestion_fee) AS with_fee
FROM iceberg.nyc.yellow_trips
GROUP BY 1 ORDER BY 1;