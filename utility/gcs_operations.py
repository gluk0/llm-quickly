from google.cloud import storage
import os
import logging

logger = logging.getLogger('llm-quickly')

class GCSUploader:
    def __init__(self, bucket_name: str):
        """Initialize GCS uploader with bucket name."""
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def upload_directory(self, local_path: str, gcs_path: str) -> None:
        """Upload an entire directory to GCS."""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"Local path does not exist: {local_path}")

        for root, _, files in os.walk(local_path):
            for file in files:
                local_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_file_path, local_path)
                blob_path = os.path.join(gcs_path, relative_path)
                
                blob = self.bucket.blob(blob_path)
                blob.upload_from_filename(local_file_path)
                logger.info(f"Uploaded {local_file_path} to gs://{self.bucket_name}/{blob_path}")


class GCSDownloader:
    def __init__(self, bucket_name: str):
        """Initialize GCS downloader with bucket name."""
        self.client = storage.Client()
        self.bucket_name = bucket_name
        self.bucket = self.client.bucket(bucket_name)

    def download_directory(self, gcs_path: str, local_path: str) -> None:
        """Download an entire directory from GCS."""
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        blobs = self.bucket.list_blobs(prefix=gcs_path)
        for blob in blobs:
            relative_path = os.path.relpath(blob.name, gcs_path)
            local_file_path = os.path.join(local_path, relative_path)
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            
            blob.download_to_filename(local_file_path)
            logger.info(f"Downloaded gs://{self.bucket_name}/{blob.name} to {local_file_path}")