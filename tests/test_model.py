import pytest
from unittest.mock import Mock, patch
from app.core.model import ModelManager
import torch
from google.cloud import storage

@pytest.fixture
def model_manager():
    return ModelManager(
        bucket_name="test-bucket",
        model_folder="test-model",
        local_path="/tmp/test-model"
    )

@pytest.fixture
def mock_storage_client():
    with patch('google.cloud.storage.Client') as mock_client:
        mock_bucket = Mock()
        mock_blob = Mock()
        mock_blob.name = "test-model/model.bin"
        mock_bucket.list_blobs.return_value = [mock_blob]
        mock_client.return_value.bucket.return_value = mock_bucket
        yield mock_client

@pytest.fixture
def mock_tokenizer():
    with patch('transformers.AutoTokenizer.from_pretrained') as mock:
        mock_tokenizer = Mock()
        mock_tokenizer.eos_token_id = 50256
        mock.return_value = mock_tokenizer
        yield mock

@pytest.fixture
def mock_model():
    with patch('transformers.AutoModelForCausalLM.from_pretrained') as mock:
        mock_model = Mock()
        mock_model.generate.return_value = torch.tensor([[1, 2, 3]])
        mock.return_value = mock_model
        yield mock

class TestModelManager:
    def test_download_from_gcs(self, model_manager, mock_storage_client):
        local_path = model_manager.download_from_gcs()
        assert local_path == "/tmp/test-model"
        mock_storage_client.assert_called_once()

    def test_load_model(self, model_manager, mock_storage_client, mock_tokenizer, mock_model):
        model, tokenizer = model_manager.load_model()
        assert model is not None
        assert tokenizer is not None
        mock_tokenizer.assert_called_once()
        mock_model.assert_called_once()

    def test_generate(self, model_manager, mock_tokenizer, mock_model):
        # Setup
        model_manager.model = mock_model.return_value
        model_manager.tokenizer = mock_tokenizer.return_value
        mock_tokenizer.return_value.decode.return_value = "<|system|>You are a helpful AI assistant.</s><|user|>test prompt</s><|assistant|>test response"

        # Test
        response = model_manager.generate(
            prompt="test prompt",
            max_length=100,
            temperature=0.7,
            top_p=0.9
        )

        assert response == "test response"
        mock_model.return_value.generate.assert_called_once() 