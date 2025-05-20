import pytest
from fastapi.testclient import TestClient
from datetime import datetime
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.main import app
from config.simulation_config import *

client = TestClient(app)

def test_read_main():
    """Test the main API endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "version" in data
    assert "description" in data

def test_get_scenarios():
    """Test the scenarios endpoint"""
    response = client.get("/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert "baseline" in data
    assert "climate_change" in data
    assert "technology_adoption" in data

def test_get_regions():
    """Test the regions endpoint"""
    response = client.get("/regions")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(DISTRICTS)
    for region in data:
        assert "name" in region
        assert region["name"] in DISTRICTS

def test_get_crops():
    """Test the crops endpoint"""
    response = client.get("/crops")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(CROPS)
    for crop in data:
        assert "name" in crop
        assert "base_yield" in crop

def test_get_policies():
    """Test the policies endpoint"""
    response = client.get("/policies")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    for policy in data:
        assert "name" in policy
        assert "budget" in policy

def test_simulate_endpoint():
    """Test the simulation endpoint"""
    simulation_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "scenario": "baseline",
        "districts": ["Dhaka", "Chittagong"],
        "farmer_count": 1000,
        "infrastructure": ["irrigation", "storage"],
        "policy_count": 5
    }
    
    response = client.post("/simulate", json=simulation_data)
    assert response.status_code == 200
    data = response.json()
    
    # Check that results contain the expected data
    assert "results" in data
    assert "visualizations" in data
    
    # Check that results contain data for each date
    results = data["results"]
    assert len(results) > 0
    for date, regions in results.items():
        assert isinstance(date, str)
        for region, metrics in regions.items():
            assert "climate_impact" in metrics
            assert "production" in metrics
            assert "market_price" in metrics

def test_simulate_endpoint_invalid_data():
    """Test the simulation endpoint with invalid data"""
    # Test with invalid dates
    invalid_data = {
        "start_date": "invalid-date",
        "end_date": "2024-12-31",
        "scenario": "baseline",
        "districts": ["Dhaka"],
        "farmer_count": 1000
    }
    
    response = client.post("/simulate", json=invalid_data)
    assert response.status_code == 422
    
    # Test with invalid scenario
    invalid_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "scenario": "invalid_scenario",
        "districts": ["Dhaka"],
        "farmer_count": 1000
    }
    
    response = client.post("/simulate", json=invalid_data)
    assert response.status_code == 422
    
    # Test with invalid districts
    invalid_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "scenario": "baseline",
        "districts": ["InvalidDistrict"],
        "farmer_count": 1000
    }
    
    response = client.post("/simulate", json=invalid_data)
    assert response.status_code == 422

def test_simulate_endpoint_different_scenarios():
    """Test the simulation endpoint with different scenarios"""
    base_data = {
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "districts": ["Dhaka"],
        "farmer_count": 1000
    }
    
    # Run baseline scenario
    baseline_data = {**base_data, "scenario": "baseline"}
    baseline_response = client.post("/simulate", json=baseline_data)
    assert baseline_response.status_code == 200
    baseline_results = baseline_response.json()["results"]
    
    # Run climate change scenario
    climate_change_data = {**base_data, "scenario": "climate_change"}
    climate_change_response = client.post("/simulate", json=climate_change_data)
    assert climate_change_response.status_code == 200
    climate_change_results = climate_change_response.json()["results"]
    
    # Results should be different
    assert baseline_results != climate_change_results
    
    # Compare final production
    baseline_production = sum(baseline_results["2024-12-31"][region]["production"]
                            for region in ["Dhaka"])
    climate_change_production = sum(climate_change_results["2024-12-31"][region]["production"]
                                  for region in ["Dhaka"])
    assert baseline_production != climate_change_production 