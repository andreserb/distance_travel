import pytest
from fastapi.testclient import TestClient
import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from main import app

# Initialize Client application
client = TestClient(app)

def test_register_location():
    location_data = {
        "name": "Test Location",
        "latitude": 39.7649,
        "longitude": -121.4294
    }
    response = client.post("/register_location", json=location_data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_register_location_invalid_data():
    location_data = {
        "name": "Test Location"
    }
    response = client.post("/register_location", json=location_data)
    #assert response.status_code == 422  #validation error

def test_calculate_distance_invalid_data():
    distance_data = {
        "location_ids": [" invalid_id"]
    }
    response = client.post("/calculate_distance", json=distance_data)
    #assert response.status_code == 404  #location not found
