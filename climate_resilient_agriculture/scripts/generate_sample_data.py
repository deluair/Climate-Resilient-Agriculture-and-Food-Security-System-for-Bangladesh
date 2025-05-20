import sys
import os
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from climate_resilient_agriculture.core.simulation_engine import SimulationEngine
from climate_resilient_agriculture.core.data_generator import DataGenerator
from climate_resilient_agriculture.analysis.visualization import SimulationVisualizer
from climate_resilient_agriculture.config.simulation_config import DISTRICTS, CROPS, POLICY_TYPES

def generate_sample_data(output_dir: str = "sample_data"):
    """Generate sample data for Bangladesh's agricultural context."""
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Generate sample climate data
    climate_data = {
        "temperature": {
            "min": 15.0,  # Winter minimum
            "max": 35.0,  # Summer maximum
            "trend": 0.02  # Annual increase in °C
        },
        "rainfall": {
            "min": 1500,  # Annual minimum (mm)
            "max": 3000,  # Annual maximum (mm)
            "monsoon_ratio": 0.8  # Proportion of annual rainfall during monsoon
        },
        "sea_level": {
            "current": 0.0,  # Current sea level (m)
            "rise_rate": 0.004  # Annual rise rate (m)
        }
    }
    
    # Save climate data
    with open(output_path / "climate_data.json", "w") as f:
        json.dump(climate_data, f, indent=2)
    
    # Generate sample farmer data
    farmers = []
    for district in DISTRICTS:
        num_farmers = random.randint(50, 200)
        for _ in range(num_farmers):
            farmer = {
                "id": f"F{len(farmers) + 1:04d}",
                "district": district,
                "land_size": round(random.uniform(0.5, 5.0), 2),  # hectares
                "income": round(random.uniform(50000, 200000), 2),  # BDT
                "education_level": random.choice(["none", "primary", "secondary", "higher"]),
                "access_to_irrigation": random.random() < 0.7,
                "access_to_credit": random.random() < 0.6,
                "technology_adoption": random.random() < 0.4
            }
            farmers.append(farmer)
    
    # Save farmer data
    with open(output_path / "farmers.json", "w") as f:
        json.dump(farmers, f, indent=2)
    
    # Generate sample crop data
    crop_data = {}
    for crop in CROPS:
        crop_data[crop] = {
            "base_yield": round(random.uniform(2.0, 5.0), 2),  # tons/hectare
            "price": round(random.uniform(20000, 50000), 2),  # BDT/ton
            "water_requirement": round(random.uniform(500, 2000), 2),  # mm/season
            "temperature_sensitivity": round(random.uniform(0.1, 0.3), 2),
            "flood_sensitivity": round(random.uniform(0.2, 0.5), 2),
            "drought_sensitivity": round(random.uniform(0.2, 0.5), 2)
        }
    
    # Save crop data
    with open(output_path / "crops.json", "w") as f:
        json.dump(crop_data, f, indent=2)
    
    # Generate sample policy data
    policy_data = {}
    for policy in POLICY_TYPES:
        policy_data[policy] = {
            "effectiveness": round(random.uniform(0.3, 0.8), 2),
            "cost": round(random.uniform(1000000, 5000000), 2),  # BDT
            "implementation_time": random.randint(1, 5),  # years
            "coverage": round(random.uniform(0.2, 0.8), 2)
        }
    
    # Save policy data
    with open(output_path / "policies.json", "w") as f:
        json.dump(policy_data, f, indent=2)
    
    print(f"Sample data generated in {output_path}")
    return output_path

def run_sample_simulations(data_dir: str = "sample_data"):
    """Run sample simulations using the generated data."""
    # Initialize simulation engine
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2025, 12, 31)
    engine = SimulationEngine(start_date, end_date)
    
    # Load sample data
    data_path = Path(data_dir)
    with open(data_path / "climate_data.json") as f:
        climate_data = json.load(f)
    with open(data_path / "farmers.json") as f:
        farmers = json.load(f)
    with open(data_path / "crops.json") as f:
        crop_data = json.load(f)
    with open(data_path / "policies.json") as f:
        policy_data = json.load(f)
    
    # Run baseline scenario
    print("\nRunning baseline scenario...")
    baseline_results = engine.run()
    
    # Run climate change scenario
    print("\nRunning climate change scenario...")
    climate_change_results = engine.run()
    
    # Run technology adoption scenario
    print("\nRunning technology adoption scenario...")
    tech_adoption_results = engine.run()
    
    # Save results
    results = {
        "baseline": baseline_results,
        "climate_change": climate_change_results,
        "technology_adoption": tech_adoption_results
    }
    
    with open(data_path / "simulation_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSimulation results saved to {data_path / 'simulation_results.json'}")
    
    # Generate visualizations
    viz = SimulationVisualizer()
    viz.generate_comparison_plots(results, output_dir=data_path)
    print(f"Visualizations saved to {data_path}")

if __name__ == "__main__":
    data_dir = generate_sample_data()
    run_sample_simulations(data_dir) 