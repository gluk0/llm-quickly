import argparse
from utility.setup.model import download_model, upload_to_gcs, cleanup
from utility.setup.gcp import setup_gcp

def main():
    parser = argparse.ArgumentParser(description='LLM Quickly Setup Utilities')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Setup GCP command
    gcp_parser = subparsers.add_parser('setup-gcp', help='Setup GCP resources')
    gcp_parser.add_argument('--project', default='llm-quickly-test', help='GCP project name')
    gcp_parser.add_argument('--sa-name', default='llm-quickly-sa', help='Service account name')
    gcp_parser.add_argument('--bucket', default='llm-quickly-bucket', help='Bucket name')
    
    # Upload model command
    model_parser = subparsers.add_parser('upload-model', help='Upload model to GCS')
    model_parser.add_argument('--bucket', required=True, help='GCS bucket name')
    model_parser.add_argument('--path', default='models/tinyllama', help='Path within GCS bucket')
    model_parser.add_argument(
        '--model-name', 
        default='TinyLlama/TinyLlama-1.1B-Chat-v1.0',
        help='HuggingFace model name/path to download'
    )
    
    args = parser.parse_args()
    
    if args.command == 'setup-gcp':
        setup_gcp(args.project, args.sa_name, args.bucket)
    elif args.command == 'upload-model':
      #  local_path = download_model(model_name=args.model_name)
        upload_to_gcs(local_path, args.bucket, args.path)
        cleanup(local_path)
        print("\nSetup complete! Update your .env file with:")
        print(f"GCS_BUCKET_NAME={args.bucket}")
        print(f"GCS_MODEL_PATH={args.path}")

if __name__ == "__main__":
    main() 