"""Create the S3 buckets the project needs, if they don't exist yet.

Runs from the codespace (outside Docker) after `docker compose up`.
Safe to run any number of times: existing buckets are left alone.
"""

import sys
import time
from taxi.config import load_env, s3_client 

from botocore.exceptions import ClientError, EndpointConnectionError

BUCKETS = ["raw", "warehouse"]  # raw = files as received; warehouse = Iceberg tables


def wait_for_s3(s3, timeout_s: int = 60) -> None:
    """MinIO takes a few seconds to start; retry until it answers."""
    deadline = time.time() + timeout_s
    while True:
        try:
            s3.list_buckets()
            return
        except (EndpointConnectionError, ClientError):
            if time.time() > deadline:
                sys.exit("MinIO did not respond in time. Check: docker compose logs minio")
            time.sleep(2)


def main() -> None:
    load_env()
    s3 = s3_client()
    wait_for_s3(s3)
    existing = {b["Name"] for b in s3.list_buckets()["Buckets"]}
    for bucket in BUCKETS:
        if bucket in existing:
            print(f"bucket exists:  {bucket}")
        else:
            s3.create_bucket(Bucket=bucket)
            print(f"bucket created: {bucket}")


if __name__ == "__main__":
    main()
