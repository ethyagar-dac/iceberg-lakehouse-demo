# Iceberg Lakehouse Demo

A small, local lakehouse: NYC taxi data ingested with PyIceberg into Apache Iceberg tables on S3-compatible object storage, orchestrated with Airflow and queried with Trino.

> Status: Weekend 1, platform setup. Architecture, design decisions and demos are added as the project progresses.

## Stack

| Layer | Tool |
|---|---|
| Object storage | MinIO (community build `pgsty/minio`) |
| Table format | Apache Iceberg |
| Catalog | Iceberg REST catalog (`apache/iceberg-rest-fixture`) |
| Ingestion | Python + PyIceberg |
| Query and maintenance | Trino |
| Orchestration | Airflow (Weekend 2) |

## Quickstart (GitHub Codespaces)

1. Open the repo in a codespace. The stack starts automatically.
2. Run the smoke test:
   ```bash
   make smoke
   ```
3. Open the forwarded port 9001 (MinIO console) and browse the `warehouse` bucket.

Useful commands: `make up`, `make down`, `make ps`, `make logs`, `make trino`, `make reset`.

## Notes

- The official `minio/minio` Docker images are no longer published, so this project uses a community-maintained build. In production, object storage would be a managed service such as Amazon S3.
