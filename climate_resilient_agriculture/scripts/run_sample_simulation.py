import sys
import os
from datetime import datetime, timedelta
import json
from pathlib import Path

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from climate_resilient_agriculture.core.simulation_engine import SimulationEngine
from climate_resilient_agriculture.analysis.visualization import SimulationVisualizer
from climate_resilient_agriculture.config.simulation_config import DISTRICTS, CROPS, POLICY_TYPES

def run_sample_simulation(
    scenario: str = "climate_change",
    start_date: datetime = datetime(2020, 1, 1),
    end_date: datetime = datetime(2025, 12, 31),
    output_dir: str = "sample_output"
):
    """Run a sample simulation with specific parameters."""
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Initialize simulation engine
    engine = SimulationEngine(start_date, end_date)
    
    # Load sample data
    data_path = Path("sample_data")
    with open(data_path / "climate_data.json") as f:
        climate_data = json.load(f)
    with open(data_path / "farmers.json") as f:
        farmers = json.load(f)
    with open(data_path / "crops.json") as f:
        crop_data = json.load(f)
    with open(data_path / "policies.json") as f:
        policy_data = json.load(f)
    
    # Run simulation
    print(f"\nRunning {scenario} scenario...")
    results = engine.run_simulation(
        scenario=scenario,
        climate_data=climate_data,
        farmers=farmers,
        crop_data=crop_data,
        policy_data=policy_data
    )
    
    # Save results
    with open(output_path / f"{scenario}_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nSimulation results saved to {output_path / f'{scenario}_results.json'}")
    
    # Generate visualizations
    viz = SimulationVisualizer()
    viz.generate_comparison_plots({scenario: results}, output_dir=output_path)
    print(f"Visualizations saved to {output_path}")
    
    return results

if __name__ == "__main__":
    # Example: Run climate change scenario
    results = run_sample_simulation(
        scenario="climate_change",
        start_date=datetime(2020, 1, 1),
        end_date=datetime(2025, 12, 31),
        output_dir="sample_output"
    )
    
    # Print summary statistics
    print("\nSimulation Summary:")
    print(f"Total Production: {results['total_production']:.2f} tons")
    print(f"Average Price: {results['average_price']:.2f} BDT/ton")
    print(f"Average Risk: {results['average_risk']:.2f}")
    print(f"Total Cost: {results['total_cost']:.2f} BDT")
    print(f"Total Revenue: {results['total_revenue']:.2f} BDT")
    print(f"Net Profit: {results['net_profit']:.2f} BDT") 