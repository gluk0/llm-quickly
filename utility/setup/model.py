from transformers import AutoModelForCausalLM, AutoTokenizer
from google.cloud import storage
import os
import argparse
from pathlib import Path

def download_model(model_name: str ="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    """
    Download and save a model locally
    
    Args:
        model_name (str): HuggingFace model name/path
        
    Returns:
        str: Path to saved model
    """
    print(f"Downloading model {model_name} locally...")
    local_path = "tmp_model"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(f"Saving model to {local_path}")
    model.save_pretrained(local_path)
    tokenizer.save_pretrained(local_path)
    return local_path

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