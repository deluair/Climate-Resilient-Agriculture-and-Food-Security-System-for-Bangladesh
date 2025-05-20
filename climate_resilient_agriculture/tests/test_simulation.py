import pytest
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.simulation.engine import SimulationEngine
from core.utils.data_generator import DataGenerator
from config.simulation_config import *
from core.models.base import Location, FarmerProfile, Infrastructure, Policy

def test_simulation_engine_initialization():
    """Test simulation engine initialization"""
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    time_step = timedelta(days=1)
    
    engine = SimulationEngine(start_date, end_date, time_step)
    
    assert engine.start_date == start_date
    assert engine.end_date == end_date
    assert engine.time_step == time_step
    assert engine.current_date == start_date
    assert isinstance(engine.regions, dict)
    assert isinstance(engine.farmers, dict)
    assert isinstance(engine.infrastructure, dict)
    assert isinstance(engine.policies, dict)

def test_data_generator_initialization():
    """Test data generator initialization"""
    generator = DataGenerator(seed=42)
    
    assert len(generator.DISTRICTS) > 0
    assert len(generator.AGRO_ECOLOGICAL_ZONES) > 0
    assert len(generator.CROPS) > 0
    assert len(generator.IRRIGATION_TYPES) > 0

def test_location_generation():
    """Test location generation"""
    generator = DataGenerator(seed=42)
    location = generator.generate_location("Dhaka")
    
    assert isinstance(location, Location)
    assert location.district == "Dhaka"
    assert isinstance(location.latitude, float)
    assert isinstance(location.longitude, float)
    assert location.latitude > 0
    assert location.longitude > 0
    assert location.agro_ecological_zone in generator.AGRO_ECOLOGICAL_ZONES

def test_farmer_profile_generation():
    """Test farmer profile generation"""
    generator = DataGenerator(seed=42)
    farmer = generator.generate_farmer_profile()
    
    assert isinstance(farmer, FarmerProfile)
    assert isinstance(farmer.farmer_id, str)
    assert isinstance(farmer.land_holding_size, float)
    assert farmer.land_holding_size > 0
    assert isinstance(farmer.farming_experience, int)
    assert farmer.farming_experience > 0
    assert len(farmer.crops_grown) > 0
    assert farmer.irrigation_type in generator.IRRIGATION_TYPES
    assert 0 <= farmer.technology_adoption_level <= 1
    assert 0 <= farmer.risk_tolerance <= 1

def test_infrastructure_generation():
    """Test infrastructure generation"""
    generator = DataGenerator(seed=42)
    location = generator.generate_location()
    infrastructure = generator.generate_infrastructure(location)
    
    assert isinstance(infrastructure, Infrastructure)
    assert isinstance(infrastructure.infrastructure_id, str)
    assert infrastructure.type in ["storage", "irrigation", "transportation"]
    assert infrastructure.location == location
    assert infrastructure.capacity > 0
    assert infrastructure.operational_status in ["operational", "maintenance", "under_construction"]
    assert infrastructure.maintenance_status in ["good", "fair", "poor"]

def test_policy_generation():
    """Test policy generation"""
    generator = DataGenerator(seed=42)
    policy = generator.generate_policy()
    
    assert isinstance(policy, Policy)
    assert isinstance(policy.policy_id, str)
    assert isinstance(policy.name, str)
    assert isinstance(policy.description, str)
    assert isinstance(policy.start_date, datetime)
    assert isinstance(policy.end_date, datetime)
    assert policy.target_sector in [
        "subsidy", "credit", "insurance", "technology_adoption",
        "infrastructure_development", "research_development"
    ]
    assert policy.budget_allocation > 0
    assert policy.implementation_status in ["planned", "ongoing", "completed"]
    assert isinstance(policy.success_metrics, dict)
    assert all(0 <= value <= 1 for value in policy.success_metrics.values())

def test_climate_impact_simulation():
    """Test climate impact simulation"""
    engine = SimulationEngine(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        time_step=timedelta(days=1)
    )
    
    generator = DataGenerator(seed=42)
    location = generator.generate_location("Dhaka")
    engine.add_region(location)
    
    climate_impact = engine.simulate_climate_impact("Dhaka")
    
    assert isinstance(climate_impact, dict)
    assert "temperature_change" in climate_impact
    assert "rainfall_change" in climate_impact
    assert "drought_risk" in climate_impact
    assert "flood_risk" in climate_impact
    assert 0 <= climate_impact["drought_risk"] <= 1
    assert 0 <= climate_impact["flood_risk"] <= 1

def test_crop_yield_simulation():
    """Test crop yield simulation"""
    engine = SimulationEngine(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        time_step=timedelta(days=1)
    )
    
    generator = DataGenerator(seed=42)
    farmer = generator.generate_farmer_profile()
    climate_impact = {
        "temperature_change": 0.5,
        "rainfall_change": -50,
        "drought_risk": 0.3,
        "flood_risk": 0.1
    }
    
    yield_per_hectare = engine.simulate_crop_yield(farmer, climate_impact)
    
    assert isinstance(yield_per_hectare, float)
    assert yield_per_hectare >= 0

def test_market_price_simulation():
    """Test market price simulation"""
    engine = SimulationEngine(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        time_step=timedelta(days=1)
    )
    
    production = 1000  # tons
    demand = 1100  # tons
    
    price = engine.simulate_market_prices(production, demand)
    
    assert isinstance(price, float)
    assert price > 0

def test_full_simulation():
    """Test full simulation run"""
    engine = SimulationEngine(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 1, 7),  # One week simulation
        time_step=timedelta(days=1)
    )
    
    generator = DataGenerator(seed=42)
    
    # Add a region
    location = generator.generate_location("Dhaka")
    engine.add_region(location)
    
    # Add a farmer
    farmer = generator.generate_farmer_profile()
    farmer.location = location
    engine.add_farmer(farmer)
    
    # Run simulation
    results = engine.run_full_simulation()
    
    assert isinstance(results, dict)
    assert len(results) == 7  # One week of results
    for date, region_data in results.items():
        assert isinstance(date, datetime)
        assert "Dhaka" in region_data
        assert "production" in region_data["Dhaka"]
        assert "market_price" in region_data["Dhaka"]
        assert "climate_impact" in region_data["Dhaka"] 