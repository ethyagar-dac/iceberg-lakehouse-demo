-- 1. Every commit is a snapshot. Find the last snapshot BEFORE 2025-01 was first loaded.
SELECT committed_at, snapshot_id, operation,
       element_at(summary, 'added-records')   AS added,
       element_at(summary, 'deleted-records') AS deleted,
       element_at(summary, 'total-records')   AS total
FROM iceberg.nyc."yellow_trips$snapshots"
ORDER BY committed_at;

-- 2. Current state: 3 months.
SELECT count(*) AS trips_now FROM iceberg.nyc.yellow_trips;

-- 3. Same table, as it was at that snapshot: only Nov + Dec (7,314,656 rows).
--    Replace <SNAPSHOT_ID> with the id from query 1 whose total is 7314656.
SELECT count(*) AS trips_then FROM iceberg.nyc.yellow_trips FOR VERSION AS OF <SNAPSHOT_ID>;

-- 4. Same idea by time instead of id (use a committed_at value from query 1).
-- SELECT count(*) FROM iceberg.nyc.yellow_trips FOR TIMESTAMP AS OF TIMESTAMP '2026-11-02 22:30:00 UTC';