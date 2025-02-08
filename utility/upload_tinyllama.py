from gcs_operations import GCSUploader
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('llm-quickly')

def main():
    uploader = GCSUploader(bucket_name="rich-clarke-dev-models")  
    
    try:
        uploader.upload_directory(
            local_path="../models/local/tinyllama",
            gcs_path="models/tinyllama"
        )
        logger.info("Successfully uploaded TinyLlama model to GCS")
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        logger.error("Please ensure the local model directory exists")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
