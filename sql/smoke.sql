-- Smoke test: proves Trino -> REST catalog -> MinIO works end to end.
-- Rerunnable: drops and recreates its own table.
-- After running, open the MinIO console (port 9001) -> warehouse bucket
-- and find this table's data/ and metadata/ folders.

CREATE SCHEMA IF NOT EXISTS iceberg.smoke;

DROP TABLE IF EXISTS iceberg.smoke.hello;

CREATE TABLE iceberg.smoke.hello (
    id  INTEGER,
    msg VARCHAR
);

-- Two separate inserts = two commits = two snapshots.
INSERT INTO iceberg.smoke.hello VALUES (1, 'first commit');
INSERT INTO iceberg.smoke.hello VALUES (2, 'second commit');

SELECT * FROM iceberg.smoke.hello ORDER BY id;

-- Iceberg metadata tables: every commit is a snapshot...
SELECT snapshot_id, operation, committed_at
FROM iceberg.smoke."hello$snapshots"
ORDER BY committed_at;

-- ...and every data file is tracked individually.
SELECT file_path, record_count
FROM iceberg.smoke."hello$files";
