from fastapi import APIRouter, HTTPException
from concurrent.futures import ThreadPoolExecutor
import asyncio
from app.schemas.requests import InferenceRequest, InferenceResponse
from app.core.config import get_settings
from app.core.model import ModelManager
from typing import Optional
import torch

router = APIRouter()
model_manager = None
executor = ThreadPoolExecutor(max_workers=4)

class ModelNotLoadedException(Exception):
    """Raised when model is not loaded"""
    pass

class InvalidPromptException(Exception):
    """Raised when prompt is invalid"""
    pass

@router.on_event("startup")
async def startup_event():
    """Initialize the model manager and load model on startup."""
    global model_manager
    settings = get_settings()
    model_manager = ModelManager(
        settings.gcs_bucket_name,
        settings.gcs_model_path,
        settings.local_model_path
    )
    # Loads the model from GCS on startup of the FastAPI using the router 
    # deco .on_event method so we dont need to load this into a python
    # default namespace, I find it confusing to read code like that where
    # it's not stating the 'model' is loading and you need to understand 
    # default namespaces in python to see the model is loaded. 
    model_manager.load_model()

@router.post("/inference", response_model=InferenceResponse)
async def inference(request: InferenceRequest):
    """
    Generate text based on input prompt.
    
    Args:
        request: Inference request containing prompt and generation parameters
    
    Returns:
        InferenceResponse: Generated text response
    
    Raises:
        HTTPException: With appropriate status codes for different error cases
    """
    try:
        if model_manager.model is None or model_manager.tokenizer is None:
            raise ModelNotLoadedException("Model and tokenizer must be loaded before inference")

        if not request.prompt or not request.prompt.strip():
            raise InvalidPromptException("Prompt cannot be empty")

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            executor,
            model_manager.generate,
            request.prompt,
            request.max_length,
            request.temperature,
            request.top_p
        )
        
        return InferenceResponse(generated_text=result)
    
    except ModelNotLoadedException as e:
        raise HTTPException(status_code=503, detail=str(e))
    
    except InvalidPromptException as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except torch.cuda.OutOfMemoryError:
        raise HTTPException(
            status_code=503,
            detail="GPU out of memory. Please try again later or with a shorter prompt"
        )
    
    except torch.cuda.CudaError as e:
        raise HTTPException(
            status_code=503,
            detail=f"CUDA error occurred: {str(e)}"
        )
    
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Request timed out. Please try again with a shorter prompt or different parameters"
        )
    
    except Exception as e:
        # Log unexpected errors here
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )

@router.get("/health")
async def health_check():
    """
    Check API health status.
    
    Returns:
        dict: Health status
    """
    return {"status": "healthy"} 