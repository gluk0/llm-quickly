from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from google.cloud import storage
import pathlib
import os
from typing import Tuple, Any

class ModelManager:
    """
    Manages the loading and inference of the language model.
    """
    
    def __init__(self, bucket_name: str, model_folder: str, local_path: str):
        """
        Initialize the model manager.
        Args:
            bucket_name: GCS bucket name
            model_folder: Path to model in GCS
            local_path: Local path to store model
        """
        self.bucket_name = bucket_name
        self.model_folder = model_folder
        self.local_path = local_path
        self.model = None
        self.tokenizer = None

    def download_from_gcs(self) -> str:
        """
        Downloads model files from Google Cloud Storage.
        
        Returns:
            str: Path to downloaded model files
        """
        pathlib.Path(self.local_path).mkdir(parents=True, exist_ok=True)
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket_name)
        blobs = bucket.list_blobs(prefix=self.model_folder)
        for blob in blobs:
            if blob.name.endswith('/'):
                continue 
            relative_path = blob.name.replace(self.model_folder, '')
            local_file_path = os.path.join(self.local_path, relative_path)
            os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
            blob.download_to_filename(local_file_path)
        
        return self.local_path

    def load_model(self) -> Tuple[Any, Any]:
        """
        Loads the model and tokenizer from a local path 

        Returns:
            Tuple[Any, Any]: Loaded model and tokenizer
        """
        local_path = self.download_from_gcs()

        self.tokenizer = AutoTokenizer.from_pretrained(
            local_path,
            use_fast=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            local_path,
            device_map="auto",
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True
        )
        # Needs some work this tbh, could potentially set this as an env var
        # and staticially set the device in torch rather than use the method
        # below to check if cuda is present on the host/container running the 
        # code. 
        if torch.cuda.is_available():
            self.model = self.model.to("cuda")
        
        return self.model, self.tokenizer

    def generate(self, prompt: str, max_length: int, temperature: float, top_p: float) -> str:
        """
        Generates text based on input prompt.
        
        Args:
            prompt: Input text
            max_length: Maximum length of generated text
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
        
        Returns:
            str: Generated text
        """

        # Format prompt with system and user context - this helps the model understand 
        # the role of the assistant and the inputted prompt from the fast api.
        # (this is just a simple structure to begin with for now)..... 
        formatted_prompt = f"<|system|>You are a helpful AI assistant.</s><|user|>{prompt}</s><|assistant|>"
        
        # Convert text to token ids and return as pyt tensors. 
        inputs = self.tokenizer(formatted_prompt, return_tensors="pt")
        if torch.cuda.is_available():
            inputs = inputs.to("cuda")
        
        # When we're just doing inference (generating text), we don't need to track gradients
        # which are only needed for training. no_grad() saves memory and speeds things up by
        # telling PyTorch "don't bother storing all the intermediate values needed for
        # backpropagation". It's like putting the model in 'evaluation mode' for code executed
        # in this context handler from the torch library..... 
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,  # Cap the length to avoid endless responses
                temperature=temperature,  # Higher = more creative but random, lower = more focused but repetitive
                top_p=top_p,  # Nucleus sampling - only consider tokens comprising the top_p probability mass
                pad_token_id=self.tokenizer.eos_token_id,  # Needed to properly end sequences
                do_sample=True,  # Use sampling instead of greedy decoding - makes responses more natural 
                repetition_penalty=1.2  # Penalize repetition - helps avoid loops like "I think think think..."
            )
        
        # Decode tokens back to text and clean up the response
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Only return the assistant's response, strip out the prompt
        return generated_text.split("<|assistant|>")[-1].strip() 