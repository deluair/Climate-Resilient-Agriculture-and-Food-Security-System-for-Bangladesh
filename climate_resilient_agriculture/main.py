from datetime import datetime, timedelta
import json
from pathlib import Path
from core.simulation.engine import SimulationEngine
from core.utils.data_generator import DataGenerator
from analysis.visualization import SimulationVisualizer

def main():
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    # Initialize components
    data_generator = DataGenerator(seed=42)
    visualizer = SimulationVisualizer()
    
    # Set simulation parameters
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 12, 31)
    time_step = timedelta(days=1)
    
    # Initialize simulation engine
    engine = SimulationEngine(start_date, end_date, time_step)
    
    # Generate and add regions
    print("Generating regions...")
    for district in data_generator.DISTRICTS:
        location = data_generator.generate_location(district)
        engine.add_region(location)
    
    # Generate and add farmers
    print("Generating farmers...")
    for _ in range(1000):  # Generate 1000 farmers
        farmer = data_generator.generate_farmer_profile()
        engine.add_farmer(farmer)
    
    # Generate and add infrastructure
    print("Generating infrastructure...")
    for district in data_generator.DISTRICTS:
        location = data_generator.generate_location(district)
        for _ in range(5):  # 5 infrastructure items per district
            infrastructure = data_generator.generate_infrastructure(location)
            engine.add_infrastructure(infrastructure)
    
    # Generate and add policies
    print("Generating policies...")
    for _ in range(10):  # Generate 10 policies
        policy = data_generator.generate_policy()
        engine.add_policy(policy)
    
    # Run simulation
    print("Running simulation...")
    results = engine.run_full_simulation()
    
    # Save results
    print("Saving results...")
    results_file = output_dir / "simulation_results.json"
    with open(results_file, "w") as f:
        json.dump(results, f, default=str)
    
    # Generate visualizations
    print("Generating visualizations...")
    
    # Climate impact visualization
    climate_data = {region: {date: data['climate_impact'] 
                           for date, data in results.items()}
                   for region in data_generator.DISTRICTS}
    visualizer.plot_climate_impact(climate_data, 
                                 save_path=output_dir / "climate_impact.png")
    
    # Production trends visualization
    production_data = {region: {date: {'production': data['production'],
                                     'market_price': data['market_price']}
                              for date, data in results.items()}
                      for region in data_generator.DISTRICTS}
    visualizer.plot_production_trends(production_data,
                                    save_path=output_dir / "production_trends.png")
    
    # Risk map
    locations = {region: {'latitude': engine.regions[region].latitude,
                         'longitude': engine.regions[region].longitude,
                         'drought_risk': results[end_date][region]['climate_impact']['drought_risk'],
                         'flood_risk': results[end_date][region]['climate_impact']['flood_risk']}
                for region in data_generator.DISTRICTS}
    visualizer.create_risk_map(locations,
                              save_path=output_dir / "risk_map.html")
    
    # Farmer distribution
    farmer_data = [farmer.dict() for farmer in engine.farmers.values()]
    visualizer.plot_farmer_distribution(farmer_data,
                                      save_path=output_dir / "farmer_distribution.png")
    
    # Policy impact
    policy_data = {policy.target_sector: policy.success_metrics
                  for policy in engine.policies.values()}
    visualizer.plot_policy_impact(policy_data,
                                save_path=output_dir / "policy_impact.png")
    
    # Create comprehensive dashboard
    dashboard_data = {
        'climate_data': climate_data,
        'production_data': production_data,
        'market_data': {region: {date: data['market_price']
                               for date, data in results.items()}
                       for region in data_generator.DISTRICTS},
        'policy_data': policy_data,
        'farmer_data': farmer_data,
        'risk_data': locations
    }
    visualizer.create_dashboard(dashboard_data,
                              save_path=output_dir / "dashboard.png")
    
    print("Simulation completed successfully!")
    print(f"Results saved in: {output_dir}")

if __name__ == "__main__":
    main() 