# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from src.main import app
import os
from unittest.mock import Mock, patch

# Mock response for OpenAI client
mock_response = Mock()
mock_response.chat.completions.create.return_value = {
    "choices": [{"message": {"content": "Mocked response"}}]
}

# Mock streaming response
mock_stream_response = [
    {"choices": [{"delta": {"content": "Hello"}}]},
    {"choices": [{"delta": {"content": " world"}}]},
    {"choices": [{"delta": {}}]}  # End of stream
]

# Use TestClient for synchronous tests
client = TestClient(app)

# Fixture to mock get_api_client
@pytest.fixture
def mock_client():
    with patch("src.utils.get_api_client") as mock_get_client:
        mock_client = Mock()
        mock_client.chat.completions.create.side_effect = [
            mock_response,  # For /generate/response
            mock_stream_response  # For /stream/response
        ]
        mock_get_client.return_value = mock_client
        yield mock_client

# Test the root endpoint
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

# Test the /generate/response endpoint (synchronous)
def test_generate_text_success(mock_client):
    response = client.post("/generate/response", json={"prompt": "Hi there"})
    assert response.status_code == 200
    assert "response" in response.json()
    assert response.json()["response"]["choices"][0]["message"]["content"] == "Mocked response"

def test_generate_text_missing_prompt():
    response = client.post("/generate/response", json={})
    assert response.status_code == 422  # Unprocessable Entity (validation error)
    assert "detail" in response.json()

def test_generate_text_exception(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("API error")
    response = client.post("/generate/response", json={"prompt": "Hi there"})
    assert response.status_code == 200  # FastAPI returns 200 with error in body
    assert "error" in response.json()
    assert response.json()["error"] == "API error"

# Test the /stream/response endpoint (asynchronous)
@pytest.mark.asyncio
async def test_stream_text_success(mock_client):
    async with AsyncClient(app=app, base_url="http://test") as async_client:
        response = await async_client.post("/stream/response", json={"prompt": "Hi there"})
        assert response.status_code == 200
        
        # Since this is a streaming endpoint, we can't use TestClient directly
        # Simulate streaming response handling
        content = ""
        async for chunk in response.aiter_text():
            if "response" in chunk:
                content += chunk
        assert "Hello world" in content

def test_stream_text_exception(mock_client):
    mock_client.chat.completions.create.side_effect = Exception("Stream error")
    response = client.post("/stream/response", json={"prompt": "Hi there"})
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Stream error"

# Test CORS middleware
def test_cors_headers():
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers
    assert response.headers["access-control-allow-origin"] == "*"

# Test SYSTEM_PROMPT environment variable
def test_system_prompt_default():
    assert os.getenv("SYSTEM_PROMPT", "You are a helpful assistant.") == "You are a helpful assistant."
    # Optionally set a custom SYSTEM_PROMPT for testing
    os.environ["SYSTEM_PROMPT"] = "Custom assistant"
    from src.main import SYSTEM_PROMPT
    assert SYSTEM_PROMPT == "Custom assistant"