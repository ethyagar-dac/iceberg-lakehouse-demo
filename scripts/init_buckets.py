"""Create the S3 buckets the project needs, if they don't exist yet.

Runs from the codespace (outside Docker) after `docker compose up`.
Safe to run any number of times: existing buckets are left alone.
"""

import os
import sys
import time

import boto3
from botocore.exceptions import ClientError, EndpointConnectionError

BUCKETS = ["raw", "warehouse"]  # raw = files as received; warehouse = Iceberg tables


def load_env(path: str = ".env") -> None:
    """Read KEY=VALUE lines from .env into os.environ (without overriding)."""
    if not os.path.exists(path):
        return
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key, value)


def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=os.environ["S3_ENDPOINT"],
        aws_access_key_id=os.environ["MINIO_ROOT_USER"],
        aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
        region_name=os.environ["AWS_REGION"],
    )


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
