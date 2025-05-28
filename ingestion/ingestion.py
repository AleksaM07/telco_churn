"""
Fetch latest 200 works from CrossRef, store raw JSON to local MinIO as Parquet.
"""

import os, json
from datetime import datetime
import requests
import polars as pl
import boto3
from botocore.client import Config

# ---- Config ----
CROSSREF_API = "https://api.crossref.org/works"
ROWS = 200
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS = os.getenv("MINIO_ACCESS_KEY", "minio")
MINIO_SECRET = os.getenv("MINIO_SECRET_KEY", "minio123")
BUCKET = "scilit-raw"

# ---- Fetch raw items ----
def fetch_crossref(rows=ROWS):
    resp = requests.get(CROSSREF_API, params={
        "sort": "published", "order": "desc", "rows": rows
    })
    resp.raise_for_status()
    return resp.json()["message"]["items"]

# ---- Normalize into Polars DF ----
def normalize_to_df(items):
    records = []
    for it in items:
        records.append({
            "work_id": it.get("DOI"),
            "raw": json.dumps(it),
            "ingested_at": datetime.utcnow().isoformat()
        })
    return pl.DataFrame(records)

# ---- Write Parquet locally + upload to MinIO ----
def write_parquet(df: pl.DataFrame, path: str):
    df.write_parquet(path)

def upload_to_minio(local_path, object_name):
    s3 = boto3.resource(
        "s3",
        #endpoint_url=f"http://{MINIO_ENDPOINT}",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ACCESS,
        aws_secret_access_key=MINIO_SECRET,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"
    )
    bucket = s3.Bucket(BUCKET)
    bucket.upload_file(local_path, object_name)
    print(f"Uploaded {object_name} to MinIO bucket {BUCKET}")

if __name__ == "__main__":
    items = fetch_crossref()
    df = normalize_to_df(items)

    today = datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
    BASE_DIR = os.path.dirname(__file__)
    data_dir = os.path.join(BASE_DIR, "data", "raw")
    os.makedirs(data_dir, exist_ok=True)

    local_file = os.path.join(data_dir, f"crossref_{today}.parquet")

    write_parquet(df, local_file)
    upload_to_minio(local_file, f"crossref/{os.path.basename(local_file)}")
    print(f"Done: {df.height} records ingested.")