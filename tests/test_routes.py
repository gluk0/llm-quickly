import pytest
from fastapi.testclient import TestClient
from app.api.routes import router, model_manager
from app.schemas.requests import InferenceRequest
from unittest.mock import Mock, patch

@pytest.fixture
def client():
    return TestClient(router)

@pytest.fixture
def mock_model_manager():
    with patch('app.api.routes.ModelManager') as mock:
        mock_instance = Mock()
        mock_instance.model = Mock()
        mock_instance.tokenizer = Mock()
        mock_instance.generate.return_value = "Test response"
        mock.return_value = mock_instance
        yield mock_instance

class TestRoutes:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

    def test_inference_success(self, client, mock_model_manager):
        # Setup
        global model_manager
        model_manager = mock_model_manager

        # Test
        request_data = {
            "prompt": "Test prompt",
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = client.post("/inference", json=request_data)
        
        assert response.status_code == 200
        assert response.json() == {"generated_text": "Test response"}
        mock_model_manager.generate.assert_called_once_with(
            "Test prompt", 100, 0.7, 0.9
        )

    def test_inference_empty_prompt(self, client, mock_model_manager):
        # Setup
        global model_manager
        model_manager = mock_model_manager

        # Test
        request_data = {
            "prompt": "",
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = client.post("/inference", json=request_data)
        
        assert response.status_code == 400
        assert "Prompt cannot be empty" in response.json()["detail"]

    def test_inference_model_not_loaded(self, client, mock_model_manager):
        # Setup
        global model_manager
        mock_model_manager.model = None
        mock_model_manager.tokenizer = None
        model_manager = mock_model_manager

        # Test
        request_data = {
            "prompt": "Test prompt",
            "max_length": 100,
            "temperature": 0.7,
            "top_p": 0.9
        }
        
        response = client.post("/inference", json=request_data)
        
        assert response.status_code == 503
        assert "Model and tokenizer must be loaded" in response.json()["detail"]

    @pytest.mark.asyncio
    async def test_startup_event(self, mock_model_manager):
        from app.api.routes import startup_event
        
        # Test
        await startup_event()
        mock_model_manager.load_model.assert_called_once() 