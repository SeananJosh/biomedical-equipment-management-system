import pytest
import uuid
from fastapi.testclient import TestClient
from app import app


@pytest.fixture
def sample_numbers():
    return [1, 2, 3, 4, 5]


@pytest.fixture
def equipment_data():
    return {
        "name": "Test MRI",
        "model": "MRI-100",
        "serial_number": f"TEST-{uuid.uuid4()}",
        "department": "Radiology",
        "status": "available"
    }


@pytest.fixture
def created_equipment(equipment_data):
    client = TestClient(app)

    # Setup: create equipment
    response = client.post(
        "/equipment",
        json=equipment_data
    )

    assert response.status_code == 201

    equipment = response.json()["equipment"]

    # Give the created equipment to the test
    yield equipment

    # Cleanup: delete the equipment
    client.delete(f"/equipment/{equipment['id']}")