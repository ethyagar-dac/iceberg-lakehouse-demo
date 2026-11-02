trino> SELECT snapshot_id, operation FROM iceberg.nyc."yellow_trips$snapshots" ORDER BY committed_at;
     snapshot_id     | operation 
---------------------+-----------
 2204083687466485185 | append    
 4847028515545759147 | delete    
 3576935699766960642 | append    
 4136408840516862766 | append    
 5146957657757513757 | append    
(5 rows)

Query 20261102_224035_00003_ktt29, FINISHED, 1 node
Splits: 5 total, 5 done (100.00%)
0.36 [5 rows, 3.09KiB] [13 rows/s, 8.55KiB/s]

trino> 
trino> SELECT committed_at, operation,
    ->        element_at(summary, 'added-records')   AS added,
    ->        element_at(summary, 'deleted-records') AS deleted
    -> FROM iceberg.nyc."yellow_trips$snapshots" ORDER BY committed_at;
        committed_at         | operation |  added  | deleted 
-----------------------------+-----------+---------+---------
 2026-11-02 22:36:34.363 UTC | append    | 3646319 | NULL    
 2026-11-02 22:37:31.285 UTC | delete    | NULL    | 3646319 
 2026-11-02 22:37:33.728 UTC | append    | 3646319 | NULL    
 2026-11-02 22:37:57.840 UTC | append    | 3668337 | NULL    
 2026-11-02 22:38:16.650 UTC | append    | 3475204 | NULL    
(5 rows)

Query 20261102_232833_00004_ktt29, FINISHED, 1 node
Splits: 5 total, 5 done (100.00%)
0.27 [5 rows, 3.21KiB] [18 rows/s, 11.7KiB/s]

trino> SELECT committed_at, operation,summary,
    ->        element_at(summary, 'added-records')   AS added,
    ->        element_at(summary, 'deleted-records') AS deleted
    -> FROM iceberg.nyc."yellow_trips$snapshots" ORDER BY committed_at;
        committed_at         | operation |                                                                                                                       >
-----------------------------+-----------+----------------------------------------------------------------------------------------------------------------------->
 2026-11-02 22:36:34.363 UTC | append    | {changed-partition-count=1, added-data-files=1, total-equality-deletes=0, added-records=3646319, total-position-delete>
 2026-11-02 22:37:31.285 UTC | delete    | {removed-files-size=62554687, changed-partition-count=1, total-equality-deletes=0, deleted-data-files=1, total-positio>
 2026-11-02 22:37:33.728 UTC | append    | {changed-partition-count=1, added-data-files=1, total-equality-deletes=0, added-records=3646319, total-position-delete>
 2026-11-02 22:37:57.840 UTC | append    | {changed-partition-count=1, added-data-files=1, total-equality-deletes=0, added-records=3668337, total-position-delete>
 2026-11-02 22:38:16.650 UTC | append    | {changed-partition-count=1, added-data-files=1, total-equality-deletes=0, added-records=3475204, total-position-delete>
(5 rows)

Query 20261102_232911_00005_ktt29, FINISHED, 1 node
Splits: 5 total, 5 done (100.00%)
0.26 [5 rows, 7.07KiB] [19 rows/s, 27.2KiB/s]

trino> SELECT date_trunc('month', pickup_ts) AS m, count(*) AS trips, count(cbd_congestion_fee) AS with_fee
    -> FROM iceberg.nyc.yellow_trips GROUP BY 1 ORDER BY 1;
             m              |  trips  | with_fee 
----------------------------+---------+----------
 2024-11-01 00:00:00.000000 | 3646319 |        0 
 2024-12-01 00:00:00.000000 | 3668337 |        0 
 2025-01-01 00:00:00.000000 | 3475204 |  3475204 
(3 rows)

Query 20261102_233650_00006_ktt29, FINISHED, 1 node
Splits: 20 total, 20 done (100.00%)
3.36 [10.8M rows, 47.7MiB] [3.21M rows/s, 14.2MiB/s]

trino> exit