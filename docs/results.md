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

DEMO SQL 1 : 

trino> SELECT committed_at, snapshot_id, operation,
    ->        element_at(summary, 'added-records')   AS added,
    ->        element_at(summary, 'deleted-records') AS deleted,
    ->        element_at(summary, 'total-records')   AS total
    -> FROM iceberg.nyc."yellow_trips$snapshots"
    -> ORDER BY committed_at;

        committed_at         |     snapshot_id     | operation |  added  | deleted |  total   
-----------------------------+---------------------+-----------+---------+---------+----------
 2026-11-02 22:36:34.363 UTC | 2204083687466485185 | append    | 3646319 | NULL    | 3646319  
 2026-11-02 22:37:31.285 UTC | 4847028515545759147 | delete    | NULL    | 3646319 | 0        
 2026-11-02 22:37:33.728 UTC | 3576935699766960642 | append    | 3646319 | NULL    | 3646319  
 2026-11-02 22:37:57.840 UTC | 4136408840516862766 | append    | 3668337 | NULL    | 7314656  
 2026-11-02 22:38:16.650 UTC | 5146957657757513757 | append    | 3475204 | NULL    | 10789860 
 2026-11-05 23:32:17.684 UTC | 9102596901194603785 | delete    | NULL    | 3646319 | 7143541  
 2026-11-05 23:32:21.640 UTC | 1563481728518903373 | append    | 3646319 | NULL    | 10789860 
 2026-11-06 18:56:18.133 UTC | 2708609766043024819 | delete    | NULL    | 3646319 | 7143541  
 2026-11-06 18:56:20.716 UTC | 7083988523068348450 | append    | 3646319 | NULL    | 10789860 
 2026-11-06 18:56:36.051 UTC | 6922565765139435091 | delete    | NULL    | 3668337 | 7121523  
 2026-11-06 18:56:38.675 UTC | 6869548076949421975 | append    | 3668337 | NULL    | 10789860 
 2026-11-06 18:56:48.709 UTC | 8753173867430530175 | delete    | NULL    | 3475204 | 7314656  
 2026-11-06 18:56:51.376 UTC | 3030586759111164985 | append    | 3475204 | NULL    | 10789860 
(13 rows)

Query 20261106_205518_00000_wkcs2, FINISHED, 1 node
Splits: 5 total, 5 done (100.00%)
2.40 [13 rows, 8.56KiB] [5 rows/s, 3.57KiB/s]

trino> SELECT count(*) AS trips_now FROM iceberg.nyc.yellow_trips;
 trips_now 
-----------
  10789860 
(1 row)

Query 20261106_205539_00001_wkcs2, FINISHED, 1 node
Splits: 8 total, 8 done (100.00%)
0.80 [10.8M rows, 220B] [13.5M rows/s, 275B/s]

trino> SELECT count(*) AS trips_then FROM iceberg.nyc.yellow_trips FOR VERSION AS OF 3030586759111164985;
 trips_then 
------------
   10789860
(1 row)

Query 20261106_205632_00004_wkcs2, FINISHED, 1 node
Splits: 8 total, 8 done (100.00%)
0.28 [10.8M rows, 220B] [38.8M rows/s, 791B/s]

DEMO 2: 

docker compose exec -T trino trino --output-format=ALIGNED --file /sql/demos/02_schema_evolution.sql
Nov 06, 2026 8:57:16 PM org.jline.utils.Log logr
WARNING: Unable to create a system terminal, creating a dumb terminal (enable debug logging for more information)
        Column         |     Type     | Extra | Comment 
-----------------------+--------------+-------+---------
 vendor_id             | integer      |       |         
 pickup_ts             | timestamp(6) |       |         
 dropoff_ts            | timestamp(6) |       |         
 passenger_count       | bigint       |       |         
 trip_distance         | double       |       |         
 rate_code_id          | bigint       |       |         
 store_and_fwd_flag    | varchar      |       |         
 pickup_location_id    | integer      |       |         
 dropoff_location_id   | integer      |       |         
 payment_type          | bigint       |       |         
 fare_amount           | double       |       |         
 extra                 | double       |       |         
 mta_tax               | double       |       |         
 tip_amount            | double       |       |         
 tolls_amount          | double       |       |         
 improvement_surcharge | double       |       |         
 total_amount          | double       |       |         
 congestion_surcharge  | double       |       |         
 airport_fee           | double       |       |         
 cbd_congestion_fee    | double       |       |         
(20 rows)
           month            |  trips  | with_fee 
----------------------------+---------+----------
 2024-11-01 00:00:00.000000 | 3646319 |        0 
 2024-12-01 00:00:00.000000 | 3668337 |        0 
 2025-01-01 00:00:00.000000 | 3475204 |  3475204 
(3 rows)

DEMO 3a: 

docker compose exec -T trino trino --output-format=ALIGNED --file /sql/demos/03a_partition_evolution.sql
Nov 06, 2026 8:57:53 PM org.jline.utils.Log logr
WARNING: Unable to create a system terminal, creating a dumb terminal (enable debug logging for more information)
                   Create Table                   
--------------------------------------------------
 CREATE TABLE iceberg.nyc.yellow_trips (          
    vendor_id integer,                            
    pickup_ts timestamp(6),                       
    dropoff_ts timestamp(6),                      
    passenger_count bigint,                       
    trip_distance double,                         
    rate_code_id bigint,                          
    store_and_fwd_flag varchar,                   
    pickup_location_id integer,                   
    dropoff_location_id integer,                  
    payment_type bigint,                          
    fare_amount double,                           
    extra double,                                 
    mta_tax double,                               
    tip_amount double,                            
    tolls_amount double,                          
    improvement_surcharge double,                 
    total_amount double,                          
    congestion_surcharge double,                  
    airport_fee double,                           
    cbd_congestion_fee double                     
 )                                                
 WITH (                                           
    compression_codec = 'ZSTD',                   
    format = 'PARQUET',                           
    format_version = 2,                           
    location = 's3://warehouse/nyc/yellow_trips', 
    partitioning = ARRAY['month(pickup_ts)']      
 )                                                
(1 row)
SET PROPERTIES
                   Create Table                   
--------------------------------------------------
 CREATE TABLE iceberg.nyc.yellow_trips (          
    vendor_id integer,                            
    pickup_ts timestamp(6),                       
    dropoff_ts timestamp(6),                      
    passenger_count bigint,                       
    trip_distance double,                         
    rate_code_id bigint,                          
    store_and_fwd_flag varchar,                   
    pickup_location_id integer,                   
    dropoff_location_id integer,                  
    payment_type bigint,                          
    fare_amount double,                           
    extra double,                                 
    mta_tax double,                               
    tip_amount double,                            
    tolls_amount double,                          
    improvement_surcharge double,                 
    total_amount double,                          
    congestion_surcharge double,                  
    airport_fee double,                           
    cbd_congestion_fee double                     
 )                                                
 WITH (                                           
    compression_codec = 'ZSTD',                   
    format = 'PARQUET',                           
    format_version = 2,                           
    location = 's3://warehouse/nyc/yellow_trips', 
    partitioning = ARRAY['day(pickup_ts)']        
 )                                                

DEMO 3b: 

docker compose exec -T trino trino --output-format=ALIGNED --file /sql/demos/03b_partition_evolution_check.sql
Nov 06, 2026 8:59:01 PM org.jline.utils.Log logr
WARNING: Unable to create a system terminal, creating a dumb terminal (enable debug logging for more information)
 spec_id | files |   rows   
---------+-------+----------
       1 |     5 | 10789860 
(1 row)
           month            |  trips  
----------------------------+---------
 2024-11-01 00:00:00.000000 | 3646319 
 2024-12-01 00:00:00.000000 | 3668337 
 2025-01-01 00:00:00.000000 | 3475204 
(3 rows)
                                                                                                          Query Plan                                                                                                           
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Trino version: 477                                                                                                                                                                                                            
 Queued: 2.96ms, Analysis: 35.97ms, Planning: 171.75ms, Execution: 685.06ms                                                                                                                                                    
 Fragment 1 [SINGLE]                                                                                                                                                                                                           
     CPU: 2.42ms, Scheduled: 3.88ms, Blocked 1.08s (Input: 717.03ms, Output: 0.00ns), Input: 4 rows (36B); per task: avg.: 4.00 std.dev.: 0.00, Output: 1 row (9B)                                                             
     Peak Memory: 192B, Tasks count: 1; per task: max: 216B                                                                                                                                                                    
     Output layout: [count]                                                                                                                                                                                                    
     Output partitioning: SINGLE []                                                                                                                                                                                            
     Aggregate[type = FINAL]                                                                                                                                                                                                   
     │   Layout: [count:bigint]                                                                                                                                                                                                
     │   Estimates: {rows: 1 (9B), cpu: 1017.05k, memory: 9B, network: 0B}                                                                                                                                                     
     │   CPU: 0.00ns (0.00%), Scheduled: 1.00ms (0.12%), Blocked: 0.00ns (0.00%), Output: 1 row (9B)                                                                                                                           
     │   Input avg.: 4.00 rows, Input std.dev.: 0.00%                                                                                                                                                                          
     │   count := count(count_0)                                                                                                                                                                                               
     └─ LocalExchange[partitioning = SINGLE]                                                                                                                                                                                   
        │   Layout: [count_0:bigint]                                                                                                                                                                                           
        │   Estimates: {rows: 115718 (1017.05kB), cpu: 0, memory: 0B, network: 0B}                                                                                                                                             
        │   CPU: 0.00ns (0.00%), Scheduled: 1.00ms (0.12%), Blocked: 364.00ms (33.67%), Output: 4 rows (36B)                                                                                                                   
        │   Input avg.: 2.00 rows, Input std.dev.: 0.00%                                                                                                                                                                       
        └─ RemoteSource[sourceFragmentIds = [2]]                                                                                                                                                                               
               Layout: [count_0:bigint]                                                                                                                                                                                        
               CPU: 0.00ns (0.00%), Scheduled: 0.00ns (0.00%), Blocked: 717.00ms (66.33%), Output: 4 rows (36B)                                                                                                                
               Input avg.: 2.00 rows, Input std.dev.: 0.00%                                                                                                                                                                    
                                                                                                                                                                                                                               
 Fragment 2 [SOURCE]                                                                                                                                                                                                           
     CPU: 263.75ms, Scheduled: 829.79ms, Blocked 0.00ns (Input: 0.00ns, Output: 0.00ns), Input: 2538669 rows (21.79MB); per task: avg.: 2538669.00 std.dev.: 0.00, Output: 4 rows (36B)                                        
     Peak Memory: 320B, Tasks count: 1; per task: max: 7.32MB                                                                                                                                                                  
     Output layout: [count_0]                                                                                                                                                                                                  
     Output partitioning: SINGLE []                                                                                                                                                                                            
     Aggregate[type = PARTIAL]                                                                                                                                                                                                 
     │   Layout: [count_0:bigint]                                                                                                                                                                                              
     │   Estimates: {rows: 115718 (1017.05kB), cpu: ?, memory: ?, network: ?}                                                                                                                                                  
     │   CPU: 4.00ms (1.52%), Scheduled: 15.00ms (1.80%), Blocked: 0.00ns (0.00%), Output: 4 rows (36B)                                                                                                                        
     │   Input avg.: 34547.25 rows, Input std.dev.: 156.00%                                                                                                                                                                    
     │   count_0 := count(*)                                                                                                                                                                                                   
     └─ ScanFilterProject[table = iceberg:nyc.yellow_trips$data@3030586759111164985, filterPredicate = ((pickup_ts >= timestamp(6) '2024-12-10 00:00:00.000000') AND (pickup_ts < timestamp(6) '2024-12-11 00:00:00.000000'))] 
            Layout: []                                                                                                                                                                                                         
            Estimates: {rows: 3587245 (0B), cpu: 30.79M, memory: 0B, network: 0B}/{rows: 115718 (0B), cpu: 30.79M, memory: 0B, network: 0B}/{rows: 115718 (0B), cpu: 0, memory: 0B, network: 0B}                               
            CPU: 260.00ms (98.48%), Scheduled: 815.00ms (97.96%), Blocked: 0.00ns (0.00%), Output: 138189 rows (0B)                                                                                                            
            Input avg.: 634667.25 rows, Input std.dev.: 69.70%                                                                                                                                                                 
            pickup_ts := 2:pickup_ts:timestamp(6)                                                                                                                                                                              
            Input: 2538669 rows (21.79MB), Filtered: 94.56%, Physical input: 11.47MB, Physical input time: 185.34ms, Splits: 4, Splits generation wait time: 47.49ms                                                           
                                                                                                                                                                                                                               
                                                                                                                                                                                                                               
(1 row)
                                                                                                          Query Plan                                                                                                           
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Trino version: 477                                                                                                                                                                                                            
 Queued: 2.90ms, Analysis: 27.26ms, Planning: 72.00ms, Execution: 390.58ms                                                                                                                                                     
 Fragment 1 [SINGLE]                                                                                                                                                                                                           
     CPU: 2.58ms, Scheduled: 4.28ms, Blocked 521.72ms (Input: 348.82ms, Output: 0.00ns), Input: 4 rows (36B); per task: avg.: 4.00 std.dev.: 0.00, Output: 1 row (9B)                                                          
     Peak Memory: 192B, Tasks count: 1; per task: max: 216B                                                                                                                                                                    
     Output layout: [count]                                                                                                                                                                                                    
     Output partitioning: SINGLE []                                                                                                                                                                                            
     Aggregate[type = FINAL]                                                                                                                                                                                                   
     │   Layout: [count:bigint]                                                                                                                                                                                                
     │   Estimates: {rows: 1 (9B), cpu: 1.03M, memory: 9B, network: 0B}                                                                                                                                                        
     │   CPU: 0.00ns (0.00%), Scheduled: 0.00ns (0.00%), Blocked: 0.00ns (0.00%), Output: 1 row (9B)                                                                                                                           
     │   Input avg.: 4.00 rows, Input std.dev.: 0.00%                                                                                                                                                                          
     │   count := count(count_0)                                                                                                                                                                                               
     └─ LocalExchange[partitioning = SINGLE]                                                                                                                                                                                   
        │   Layout: [count_0:bigint]                                                                                                                                                                                           
        │   Estimates: {rows: 119586 (1.03MB), cpu: 0, memory: 0B, network: 0B}                                                                                                                                                
        │   CPU: 0.00ns (0.00%), Scheduled: 2.00ms (0.48%), Blocked: 176.00ms (33.52%), Output: 4 rows (36B)                                                                                                                   
        │   Input avg.: 2.00 rows, Input std.dev.: 0.00%                                                                                                                                                                       
        └─ RemoteSource[sourceFragmentIds = [2]]                                                                                                                                                                               
               Layout: [count_0:bigint]                                                                                                                                                                                        
               CPU: 0.00ns (0.00%), Scheduled: 1.00ms (0.24%), Blocked: 349.00ms (66.48%), Output: 4 rows (36B)                                                                                                                
               Input avg.: 2.00 rows, Input std.dev.: 0.00%                                                                                                                                                                    
                                                                                                                                                                                                                               
 Fragment 2 [SOURCE]                                                                                                                                                                                                           
     CPU: 219.96ms, Scheduled: 412.87ms, Blocked 0.00ns (Input: 0.00ns, Output: 0.00ns), Input: 2538993 rows (21.79MB); per task: avg.: 2538993.00 std.dev.: 0.00, Output: 4 rows (36B)                                        
     Peak Memory: 320B, Tasks count: 1; per task: max: 7.43MB                                                                                                                                                                  
     Output layout: [count_0]                                                                                                                                                                                                  
     Output partitioning: SINGLE []                                                                                                                                                                                            
     Aggregate[type = PARTIAL]                                                                                                                                                                                                 
     │   Layout: [count_0:bigint]                                                                                                                                                                                              
     │   Estimates: {rows: 119586 (1.03MB), cpu: ?, memory: ?, network: ?}                                                                                                                                                     
     │   CPU: 2.00ms (0.91%), Scheduled: 2.00ms (0.48%), Blocked: 0.00ns (0.00%), Output: 4 rows (36B)                                                                                                                         
     │   Input avg.: 28398.50 rows, Input std.dev.: 85.86%                                                                                                                                                                     
     │   count_0 := count(*)                                                                                                                                                                                                   
     └─ ScanFilterProject[table = iceberg:nyc.yellow_trips$data@3030586759111164985, filterPredicate = ((pickup_ts >= timestamp(6) '2024-11-10 00:00:00.000000') AND (pickup_ts < timestamp(6) '2024-11-11 00:00:00.000000'))] 
            Layout: []                                                                                                                                                                                                         
            Estimates: {rows: 3587569 (0B), cpu: 30.79M, memory: 0B, network: 0B}/{rows: 119586 (0B), cpu: 30.79M, memory: 0B, network: 0B}/{rows: 119586 (0B), cpu: 0, memory: 0B, network: 0B}                               
            CPU: 217.00ms (99.09%), Scheduled: 410.00ms (98.80%), Blocked: 0.00ns (0.00%), Output: 113594 rows (0B)                                                                                                            
            Input avg.: 634748.25 rows, Input std.dev.: 69.69%                                                                                                                                                                 
            pickup_ts := 2:pickup_ts:timestamp(6)                                                                                                                                                                              
            Input: 2538993 rows (21.79MB), Filtered: 95.53%, Physical input: 11.63MB, Physical input time: 111.72ms, Splits: 4, Splits generation wait time: 25.98ms                                                           
                                                                                                                                                                                                                               
                                                                                                                                                                                                                    
(1 row)

DEMO 4: 

docker compose exec -T trino trino --output-format=ALIGNED --file /sql/demos/04_compaction.sql
Nov 06, 2026 9:00:06 PM org.jline.utils.Log logr
WARNING: Unable to create a system terminal, creating a dumb terminal (enable debug logging for more information)
DROP TABLE
SET SESSION
CREATE TABLE: 3646319 rows
RESET SESSION
 files | avg_mb 
-------+--------
   217 |    0.3 
(1 row)
ALTER TABLE EXECUTE
 rows 
------
(0 rows)
 files | avg_mb 
-------+--------
     1 |   57.4 
(1 row)
  rows   
---------
 3646319 
(1 row)
     snapshot_id     | operation |        committed_at         
---------------------+-----------+-----------------------------
 8879834078880533072 | append    | 2026-11-06 21:00:22.955 UTC 
 2970635189912602229 | replace   | 2026-11-06 21:00:31.361 UTC 
(2 rows)
ALTER TABLE EXECUTE
 rows 
------
(0 rows)
     snapshot_id     | operation |        committed_at         
---------------------+-----------+-----------------------------
 2970635189912602229 | replace   | 2026-11-06 21:00:31.361 UTC 
(1 row)
