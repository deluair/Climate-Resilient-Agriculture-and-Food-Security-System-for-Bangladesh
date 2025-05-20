from datetime import datetime, timedelta
import json
from pathlib import Path
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.simulation.engine import SimulationEngine
from core.utils.data_generator import DataGenerator
from analysis.visualization import SimulationVisualizer
from config.simulation_config import *

def run_baseline_scenario():
    """Run the baseline scenario with current conditions"""
    print("Running baseline scenario...")
    
    # Initialize components
    data_generator = DataGenerator(seed=42)
    visualizer = SimulationVisualizer()
    
    # Initialize simulation engine
    engine = SimulationEngine(
        SIMULATION_START_DATE,
        SIMULATION_END_DATE,
        SIMULATION_TIME_STEP
    )
    
    # Generate and add regions
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        engine.add_region(location)
    
    # Generate and add farmers
    for _ in range(FARMER_COUNT):
        farmer = data_generator.generate_farmer_profile()
        engine.add_farmer(farmer)
    
    # Generate and add infrastructure
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        for _ in range(INFRASTRUCTURE_PER_DISTRICT):
            infrastructure = data_generator.generate_infrastructure(location)
            engine.add_infrastructure(infrastructure)
    
    # Generate and add policies
    for _ in range(POLICY_COUNT):
        policy = data_generator.generate_policy()
        engine.add_policy(policy)
    
    # Run simulation
    results = engine.run_full_simulation()
    
    # Save results
    output_dir = Path(OUTPUT_DIRECTORY) / "baseline"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "simulation_results.json", "w") as f:
        json.dump(results, f, default=str)
    
    # Generate visualizations
    generate_visualizations(results, output_dir, visualizer)
    
    return results

def run_climate_change_scenario():
    """Run scenario with increased climate change impacts"""
    print("Running climate change scenario...")
    
    # Initialize components
    data_generator = DataGenerator(seed=42)
    visualizer = SimulationVisualizer()
    
    # Initialize simulation engine with modified climate parameters
    engine = SimulationEngine(
        SIMULATION_START_DATE,
        SIMULATION_END_DATE,
        SIMULATION_TIME_STEP
    )
    
    # Modify climate parameters for more severe impacts
    engine.TEMPERATURE_CHANGE_MEAN = TEMPERATURE_CHANGE_MEAN * 2
    engine.RAINFALL_CHANGE_MEAN = RAINFALL_CHANGE_MEAN * 2
    
    # Generate and add regions
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        engine.add_region(location)
    
    # Generate and add farmers
    for _ in range(FARMER_COUNT):
        farmer = data_generator.generate_farmer_profile()
        engine.add_farmer(farmer)
    
    # Generate and add infrastructure
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        for _ in range(INFRASTRUCTURE_PER_DISTRICT):
            infrastructure = data_generator.generate_infrastructure(location)
            engine.add_infrastructure(infrastructure)
    
    # Generate and add policies
    for _ in range(POLICY_COUNT):
        policy = data_generator.generate_policy()
        engine.add_policy(policy)
    
    # Run simulation
    results = engine.run_full_simulation()
    
    # Save results
    output_dir = Path(OUTPUT_DIRECTORY) / "climate_change"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "simulation_results.json", "w") as f:
        json.dump(results, f, default=str)
    
    # Generate visualizations
    generate_visualizations(results, output_dir, visualizer)
    
    return results

def run_technology_adoption_scenario():
    """Run scenario with increased technology adoption"""
    print("Running technology adoption scenario...")
    
    # Initialize components
    data_generator = DataGenerator(seed=42)
    visualizer = SimulationVisualizer()
    
    # Initialize simulation engine
    engine = SimulationEngine(
        SIMULATION_START_DATE,
        SIMULATION_END_DATE,
        SIMULATION_TIME_STEP
    )
    
    # Generate and add regions
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        engine.add_region(location)
    
    # Generate and add farmers with higher technology adoption
    for _ in range(FARMER_COUNT):
        farmer = data_generator.generate_farmer_profile()
        farmer.technology_adoption_level = min(1.0, farmer.technology_adoption_level * 1.5)
        engine.add_farmer(farmer)
    
    # Generate and add infrastructure
    for district in DISTRICTS:
        location = data_generator.generate_location(district)
        for _ in range(INFRASTRUCTURE_PER_DISTRICT):
            infrastructure = data_generator.generate_infrastructure(location)
            engine.add_infrastructure(infrastructure)
    
    # Generate and add policies with focus on technology
    for _ in range(POLICY_COUNT):
        policy = data_generator.generate_policy()
        policy.target_sector = "technology_adoption"
        engine.add_policy(policy)
    
    # Run simulation
    results = engine.run_full_simulation()
    
    # Save results
    output_dir = Path(OUTPUT_DIRECTORY) / "technology_adoption"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(output_dir / "simulation_results.json", "w") as f:
        json.dump(results, f, default=str)
    
    # Generate visualizations
    generate_visualizations(results, output_dir, visualizer)
    
    return results

def generate_visualizations(results: dict, output_dir: Path, visualizer: SimulationVisualizer):
    """Generate all visualizations for the simulation results"""
    # Climate impact visualization
    climate_data = {region: {date: data['climate_impact'] 
                           for date, data in results.items()}
                   for region in DISTRICTS}
    visualizer.plot_climate_impact(climate_data, 
                                 save_path=output_dir / "climate_impact.png")
    
    # Production trends visualization
    production_data = {region: {date: {'production': data['production'],
                                     'market_price': data['market_price']}
                              for date, data in results.items()}
                      for region in DISTRICTS}
    visualizer.plot_production_trends(production_data,
                                    save_path=output_dir / "production_trends.png")
    
    # Risk map
    locations = {region: {'latitude': results[SIMULATION_START_DATE][region]['latitude'],
                         'longitude': results[SIMULATION_START_DATE][region]['longitude'],
                         'drought_risk': results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'],
                         'flood_risk': results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']}
                for region in DISTRICTS}
    visualizer.create_risk_map(locations,
                              save_path=output_dir / "risk_map.html")
    
    # Create comprehensive dashboard
    dashboard_data = {
        'climate_data': climate_data,
        'production_data': production_data,
        'market_data': {region: {date: data['market_price']
                               for date, data in results.items()}
                       for region in DISTRICTS},
        'risk_data': locations
    }
    visualizer.create_dashboard(dashboard_data,
                              save_path=output_dir / "dashboard.png")

def main():
    """Run all scenarios and compare results"""
    # Create output directory
    output_dir = Path(OUTPUT_DIRECTORY)
    output_dir.mkdir(exist_ok=True)
    
    # Run scenarios
    baseline_results = run_baseline_scenario()
    climate_change_results = run_climate_change_scenario()
    technology_adoption_results = run_technology_adoption_scenario()
    
    # Compare results
    comparison = {
        'baseline': {
            'total_production': sum(baseline_results[SIMULATION_END_DATE][region]['production']
                                  for region in DISTRICTS),
            'average_price': sum(baseline_results[SIMULATION_END_DATE][region]['market_price']
                               for region in DISTRICTS) / len(DISTRICTS),
            'average_risk': sum((baseline_results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'] +
                               baseline_results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']) / 2
                              for region in DISTRICTS) / len(DISTRICTS)
        },
        'climate_change': {
            'total_production': sum(climate_change_results[SIMULATION_END_DATE][region]['production']
                                  for region in DISTRICTS),
            'average_price': sum(climate_change_results[SIMULATION_END_DATE][region]['market_price']
                               for region in DISTRICTS) / len(DISTRICTS),
            'average_risk': sum((climate_change_results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'] +
                               climate_change_results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']) / 2
                              for region in DISTRICTS) / len(DISTRICTS)
        },
        'technology_adoption': {
            'total_production': sum(technology_adoption_results[SIMULATION_END_DATE][region]['production']
                                  for region in DISTRICTS),
            'average_price': sum(technology_adoption_results[SIMULATION_END_DATE][region]['market_price']
                               for region in DISTRICTS) / len(DISTRICTS),
            'average_risk': sum((technology_adoption_results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'] +
                               technology_adoption_results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']) / 2
                              for region in DISTRICTS) / len(DISTRICTS)
        }
    }
    
    # Save comparison results
    with open(output_dir / "scenario_comparison.json", "w") as f:
        json.dump(comparison, f, indent=4)
    
    print("\nScenario Comparison Results:")
    print("============================")
    for scenario, metrics in comparison.items():
        print(f"\n{scenario.upper()} SCENARIO:")
        print(f"Total Production: {metrics['total_production']:.2f} tons")
        print(f"Average Price: {metrics['average_price']:.2f} BDT/ton")
        print(f"Average Risk: {metrics['average_risk']:.2%}")

if __name__ == "__main__":
    main() 