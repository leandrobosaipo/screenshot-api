import pytest
from fastapi.testclient import TestClient
from main import app
import os
import time

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_screenshot_basic():
    # Testa captura básica
    response = client.post(
        "/screenshot",
        json={"url": "https://www.google.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "processing"

    # Aguarda processamento
    task_id = data["task_id"]
    max_retries = 10
    for _ in range(max_retries):
        time.sleep(2)
        status_response = client.get(f"/screenshot/status/{task_id}")
        if status_response.status_code == 200:
            break
    else:
        pytest.fail("Screenshot não foi processado no tempo esperado")

    # Verifica resultado
    assert status_response.status_code == 200
    result = status_response.json()
    assert "status" in result
    assert result["status"] in ["completed", "processing"] 