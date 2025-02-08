import argparse
import logging
from utility.setup.model import download_model, upload_to_gcs, cleanup
from utility.setup.gcp import setup_gcp

# Configure logging
logging.basicConfig(
    format='%(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger('llm-quickly')

def main():
    parser = argparse.ArgumentParser(description='LLM Quickly Setup Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # ArgParse param definitions for creating GCP resources
    # from gcloud SDK cli, long term will attempt to create 
    # a terraform wrapper and modules to auto-deploy. 
    gcp_parser = subparsers.add_parser('setup-gcp', help='Setup GCP resources')
    gcp_parser.add_argument('--project', default='llm-quickly-test', help='GCP project name')
    gcp_parser.add_argument('--sa-name', default='llm-quickly-sa', help='Service account name')
    gcp_parser.add_argument('--bucket', default='llm-quickly-bucket', help='Bucket name')
    
    model_parser = subparsers.add_parser('upload-model', help='Upload model to GCS')
    model_parser.add_argument('--bucket', required=True, help='GCS bucket name')
    model_parser.add_argument('--path', default='models/local/tinyllama', help='Path within GCS bucket')
    model_parser.add_argument(
        '--model-name', 
        default='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        help='HuggingFace model name/path to download'
    )
    
    download_parser = subparsers.add_parser('download-model', help='Download model from HuggingFace')
    download_parser.add_argument('--model-name', required=True, help='HuggingFace model name/path')
    download_parser.add_argument('--path', required=True, help='Local path to save model')
    
    args = parser.parse_args()
    
    if args.command == 'setup-gcp':
        logger.info("Setting up GCP resources...")
        setup_gcp(args.project, args.sa_name, args.bucket)
        logger.info("GCP setup completed successfully")

    elif args.command == 'upload-model':
        logger.info(f"Uploading model from {args.path} to GCS bucket {args.bucket}...")
        upload_to_gcs(args.bucket, args.path)
        logger.info("Model upload completed successfully")
        logger.info("Update your .env file with the following:")
        
        logger.info(f"GCS_BUCKET_NAME={args.bucket}")
        logger.info(f"GCS_MODEL_PATH={args.path}")

    elif args.command == 'download-model':
        logger.info(f"Downloading model {args.model_name} to {args.path}...")
        download_model(args.model_name, args.path)
        logger.info(f"Model downloaded successfully to {args.path}")

if __name__ == "__main__":
    main() 