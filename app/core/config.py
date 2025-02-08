from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application settings and environment variables configuration.
    
    Attributes:
        gcs_bucket_name: Name of the Google Cloud Storage bucket
        gcs_model_path: Path to model files within the GCS bucket
        local_model_path: Local path where model files will be stored
        model_name: Name of the model to be loaded
    """
    gcs_bucket_name: str
    gcs_model_path: str
    local_model_path: str = "/tmp/model"
    model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    """
    Creates and caches application settings.
    
    Returns:
        Settings: Application settings instance
    """
    return Settings() 