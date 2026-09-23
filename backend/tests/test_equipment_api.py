import uuid

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_equipment():
    response = client.get("/equipment")
    data=response.json()
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert "name" in data[0]

def test_get_missing_equipment():
    # make the request here

    response = client.get("/equipment/9999")  # Assuming 9999 is an ID that doesn't exist
    assert response.status_code == 404
def test_create_equipment(equipment_data):
    response=client.post("/equipment", json=equipment_data)
    assert response.status_code == 201
def test_update_equipment(created_equipment):
    equipment_id = created_equipment["id"]
    update_data = {
        "name": "Updated MRI",
        "model": "MRI-200",
        "serial_number": f"UPDATED-{uuid.uuid4()}",
        "department": "Radiology",
        "status": "maintenance"
    }
    response = client.put(
        f"/equipment/{equipment_id}",
        json=update_data
    )

    assert response.status_code == 200
def test_delete_equipment(created_equipment):
    equipment_id = created_equipment["id"]

    response = client.delete(
        f"/equipment/{equipment_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/equipment/{equipment_id}"
    )

    assert response.status_code == 404

def test_patch_equipment(created_equipment):
    equipment_id = created_equipment["id"]

    patch_data = {
        "status": "maintenance"
    }

    response = client.patch(
        f"/equipment/{equipment_id}",
        json=patch_data
    )

    assert response.status_code == 200

    updated_equipment = response.json()["equipment"]

    assert updated_equipment["status"] == "maintenance"
    assert updated_equipment["name"] == created_equipment["name"]

def test_patch_missing_equipment():
    patch_data = {
        "status": "maintenance"
    }

    response = client.patch(
        "/equipment/9999",
        json=patch_data
    )

    assert response.status_code == 404
def test_create_maintenance(created_equipment):
    equipment_id = created_equipment["id"]

    maintenance_data = {
        "description": "Routine inspection"
    }

    response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json=maintenance_data
    )

    assert response.status_code == 201

    data = response.json()

    assert data["description"] == "Routine inspection"
    assert data["equipment_id"] == equipment_id

def test_get_maintenance(created_equipment):
    equipment_id = created_equipment["id"]

    maintenance_data = {
        "description": "Routine inspection"
    }

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json=maintenance_data
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/equipment/{equipment_id}/maintenance"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert data[-1]["description"] == "Routine inspection"
    assert data[-1]["equipment_id"] == equipment_id    

def test_get_maintenance_missing_equipment():
    response = client.get(
        "/equipment/9999/maintenance"
    )

    assert response.status_code == 404
def test_get_maintenance_by_id(created_equipment):
    equipment_id = created_equipment["id"]

    maintenance_data = {
        "description": "Annual calibration"
    }

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json=maintenance_data
    )

    assert create_response.status_code == 201

    maintenance_id = create_response.json()["id"]

    response = client.get(
        f"/maintenance/{maintenance_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == maintenance_id
    assert data["equipment_id"] == equipment_id
    assert data["description"] == "Annual calibration"


def test_get_missing_maintenance():
    response = client.get("/maintenance/9999")

    assert response.status_code == 404


def test_update_maintenance(created_equipment):
    equipment_id = created_equipment["id"]

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json={
            "description": "Initial inspection"
        }
    )

    assert create_response.status_code == 201

    maintenance_id = create_response.json()["id"]

    update_response = client.put(
        f"/maintenance/{maintenance_id}",
        json={
            "description": "Updated inspection"
        }
    )

    assert update_response.status_code == 200

    data = update_response.json()

    assert data["id"] == maintenance_id
    assert data["description"] == "Updated inspection"
    assert data["equipment_id"] == equipment_id


def test_update_missing_maintenance():
    response = client.put(
        "/maintenance/9999",
        json={
            "description": "Updated inspection"
        }
    )

    assert response.status_code == 404


def test_delete_maintenance(created_equipment):
    equipment_id = created_equipment["id"]

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json={
            "description": "Maintenance to delete"
        }
    )

    assert create_response.status_code == 201

    maintenance_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/maintenance/{maintenance_id}"
    )

    assert delete_response.status_code == 204

    get_response = client.get(
        f"/maintenance/{maintenance_id}"
    )

    assert get_response.status_code == 404


def test_delete_missing_maintenance():
    response = client.delete("/maintenance/9999")

    assert response.status_code == 404

def test_equipment_with_maintenance():
    response = client.get(
        "/equipment-with-maintenance"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]
        assert "description" in data[0]


def test_equipment_maintenance_details(created_equipment):
    equipment_id = created_equipment["id"]

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json={
            "description": "Detailed maintenance test"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/equipment/{equipment_id}/maintenance-details"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    assert any(
        record["description"] == "Detailed maintenance test"
        for record in data
    )


def test_all_equipment_maintenance():
    response = client.get(
        "/all-equipment-maintenance"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


def test_equipment_maintenance_count():
    response = client.get(
        "/equipment-maintenance-count"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 0:
        assert "name" in data[0]
        assert "maintenance_count" in data[0]

def test_get_equipment_with_maintenance(created_equipment):
    equipment_id = created_equipment["id"]

    create_response = client.post(
        f"/equipment/{equipment_id}/maintenance",
        json={
            "description": "Full equipment test"
        }
    )

    assert create_response.status_code == 201

    response = client.get(
        f"/equipment/{equipment_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == equipment_id
    assert data["name"] == created_equipment["name"]
    assert "maintenance_records" in data

    assert any(
        record["description"] == "Full equipment test"
        for record in data["maintenance_records"]
    )

def test_create_equipment_invalid_status():
    equipment_data = {
        "name": "Security Test MRI",
        "model": "MRI-SEC",
        "serial_number": "SEC-TEST-001",
        "department": "Radiology",
        "status": "banana"
    }

    response = client.post(
        "/equipment",
        json=equipment_data
    )

    assert response.status_code == 422

def test_patch_equipment_invalid_status(created_equipment):
    equipment_id = created_equipment["id"]

    response = client.patch(
        f"/equipment/{equipment_id}",
        json={
            "status": "banana"
        }
    )

    assert response.status_code == 422
def test_invalid_equipment_id():
    response = client.get("/equipment/abc")

    assert response.status_code == 422

def test_duplicate_serial_number():
    serial_number = f"DUPLICATE-TEST-{uuid.uuid4()}"

    equipment_data = {
        "name": "Test MRI",
        "model": "MRI-100",
        "serial_number": serial_number,
        "department": "Radiology",
        "status": "available"
    }

    first_response = client.post(
        "/equipment",
        json=equipment_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/equipment",
        json=equipment_data
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Serial number already exists"

    equipment_id = first_response.json()["equipment"]["id"]

    client.delete(f"/equipment/{equipment_id}")