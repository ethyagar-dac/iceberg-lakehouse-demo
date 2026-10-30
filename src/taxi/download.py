"""Land one month of NYC TLC yellow taxi data in s3://raw, unchanged."""

import sys
import urllib.request

from botocore.exceptions import ClientError

from taxi.config import RAW_BUCKET, TLC_URL, load_env, s3_client


def raw_key(month: str) -> str:
    """Return the S3 key for a month, e.g. 'yellow/2024-11/yellow_tripdata_2024-11.parquet'."""
    return f"yellow/{month}/yellow_tripdata_{month}.parquet"


def exists(s3, bucket: str, key: str) -> bool:
    """True if the object is already in the bucket."""
    try:
        s3.head_object(Bucket=bucket, Key=key)
        return True
    except ClientError as e:
        if e.response["Error"]["Code"] == "404":
            return False
        raise


def download(month: str) -> None:
    load_env()
    s3 = s3_client()
    key = raw_key(month)

    if exists(s3, RAW_BUCKET, key):
        print(f"skip: s3://{RAW_BUCKET}/{key} already exists")
        return

    url = TLC_URL.format(month=month)
    print(f"downloading {url}")
    with urllib.request.urlopen(url) as resp:
        s3.upload_fileobj(resp, RAW_BUCKET, key)
    print(f"uploaded: s3://{RAW_BUCKET}/{key}")


if __name__ == "__main__":
    download(sys.argv[1])  # usage: python -m taxi.download 2024-11
