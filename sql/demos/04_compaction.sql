-- Rerunnable.
DROP TABLE IF EXISTS iceberg.nyc.compaction_demo;

-- 1. Create the small-files problem on purpose: cap file size at 2 MB while writing one month.
SET SESSION iceberg.target_max_file_size = '2MB';
CREATE TABLE iceberg.nyc.compaction_demo
WITH (partitioning = ARRAY['month(pickup_ts)'])
AS SELECT * FROM iceberg.nyc.yellow_trips
WHERE pickup_ts >= TIMESTAMP '2024-11-01 00:00:00' AND pickup_ts < TIMESTAMP '2024-12-01 00:00:00';
RESET SESSION iceberg.target_max_file_size;

-- Before: many small files.
SELECT count(*) AS files, round(avg(file_size_in_bytes) / 1e6, 1) AS avg_mb
FROM iceberg.nyc."compaction_demo$files";

-- 2. Compact: rewrite the small files into fewer large ones (a new snapshot).
ALTER TABLE iceberg.nyc.compaction_demo EXECUTE optimize;

-- After: a handful of large files. Row count unchanged.
SELECT count(*) AS files, round(avg(file_size_in_bytes) / 1e6, 1) AS avg_mb
FROM iceberg.nyc."compaction_demo$files";
SELECT count(*) AS rows FROM iceberg.nyc.compaction_demo;

-- The small files still exist on storage: the OLD snapshot references them.
SELECT snapshot_id, operation, committed_at FROM iceberg.nyc."compaction_demo$snapshots" ORDER BY committed_at;

-- 3. Expire old snapshots: deletes files no snapshot references anymore.
ALTER TABLE iceberg.nyc.compaction_demo EXECUTE expire_snapshots(retention_threshold => '0s');

-- Only the current snapshot is left; time travel to the pre-compaction state is now gone.
SELECT snapshot_id, operation, committed_at FROM iceberg.nyc."compaction_demo$snapshots" ORDER BY committed_at;