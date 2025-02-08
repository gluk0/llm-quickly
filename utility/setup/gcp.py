import subprocess
from pathlib import Path

def setup_gcp(project_name: str = "llm-quickly-test", 
              sa_name: str = "llm-quickly-sa",
              bucket_name: str = "llm-quickly-bucket"):
    """Sets up GCP project, service account, and bucket
       with the lack of terraform... 
    Args:
        project_name (str): Name of the GCP project
        sa_name (str): Name of the service account
        bucket_name (str): Name of the bucket
    """
    
    commands = [
        f"gcloud iam service-accounts create {sa_name} "
        f"--description='Service account for LLM Quickly' "
        f"--display-name='LLM Quickly SA'",
        f"gcloud iam service-accounts keys create service-account-key.json "
        f"--iam-account={sa_name}@{project_name}.iam.gserviceaccount.com",
        f"gsutil mb gs://{bucket_name}"
    ]
    
    for cmd in commands:
        try:
            subprocess.run(cmd.split(), check=True)
            print(f"Successfully executed: {cmd}")
        except subprocess.CalledProcessError as e:
            print(f"Error executing {cmd}: {e}") 