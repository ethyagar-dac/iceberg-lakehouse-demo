"""Shared settings and clients for the taxi pipeline."""

import os

import boto3
from pyarrow import fs
from pyiceberg.catalog import load_catalog

RAW_BUCKET = "raw"
TLC_URL = (
    "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"
)

NAMESPACE = "nyc"
TABLE = "nyc.yellow_trips"


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
    """boto3 S3 client pointed at MinIO."""
    return boto3.client(
        "s3",
        endpoint_url=os.environ["S3_ENDPOINT"],
        aws_access_key_id=os.environ["MINIO_ROOT_USER"],
        aws_secret_access_key=os.environ["MINIO_ROOT_PASSWORD"],
        region_name=os.environ["AWS_REGION"],
    )


def get_catalog():
    """Connect PyIceberg to the REST catalog, and to MinIO for the data files."""
    return load_catalog(
        "default",
        type="rest",
        uri=os.environ["CATALOG_URI"],  # http://localhost:8181
        # Passed as a dict because the property names contain dots.
        **{
            "s3.endpoint": os.environ["S3_ENDPOINT"],  # http://localhost:9000
            "s3.access-key-id": os.environ["MINIO_ROOT_USER"],
            "s3.secret-access-key": os.environ["MINIO_ROOT_PASSWORD"],
            "s3.region": os.environ["AWS_REGION"],
        },
    )


def arrow_s3fs() -> fs.S3FileSystem:
    """pyarrow filesystem for reading files from MinIO (used by load and quality)."""
    return fs.S3FileSystem(
        endpoint_override=os.environ["S3_ENDPOINT"].removeprefix("http://"),
        scheme="http",
        access_key=os.environ["MINIO_ROOT_USER"],
        secret_key=os.environ["MINIO_ROOT_PASSWORD"],
    )
