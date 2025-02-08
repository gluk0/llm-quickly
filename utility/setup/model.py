from transformers import AutoModelForCausalLM, AutoTokenizer
from google.cloud import storage
import os
import argparse
from pathlib import Path

def upload_to_gcs(local_path: str, bucket_name: str, gcs_path: str):

    print(f"Uploading model to GCS bucket: {bucket_name}")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    for local_file in Path(local_path).glob('**/*'):
        if local_file.is_file():
            relative_path = local_file.relative_to(local_path)
            blob_path = f"{gcs_path}/{relative_path}"
            blob = bucket.blob(blob_path)
            
            print(f"Uploading {local_file} to {blob_path}")
            blob.upload_from_filename(str(local_file))

def cleanup(local_path: str):
    print(f"Cleaning up local files in {local_path}")
    os.system(f"rm -rf {local_path}") 