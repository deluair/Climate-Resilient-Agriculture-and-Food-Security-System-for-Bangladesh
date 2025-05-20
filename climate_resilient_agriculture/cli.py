import click
import json
from datetime import datetime
from pathlib import Path
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.simulation.engine import SimulationEngine
from core.utils.data_generator import DataGenerator
from analysis.visualization import SimulationVisualizer
from config.simulation_config import *
from scripts.run_scenarios import (
    run_baseline_scenario,
    run_climate_change_scenario,
    run_technology_adoption_scenario
)

@click.group()
def cli():
    """Climate-Resilient Agriculture Simulation CLI"""
    pass

@cli.command()
@click.option('--scenario', type=click.Choice(['baseline', 'climate_change', 'technology_adoption']),
              default='baseline', help='Scenario to run')
@click.option('--start-date', type=click.DateTime(), default=SIMULATION_START_DATE,
              help='Simulation start date')
@click.option('--end-date', type=click.DateTime(), default=SIMULATION_END_DATE,
              help='Simulation end date')
@click.option('--farmer-count', type=int, default=FARMER_COUNT,
              help='Number of farmers to simulate')
@click.option('--output-dir', type=click.Path(), default=OUTPUT_DIRECTORY,
              help='Output directory for results')
def run_simulation(scenario, start_date, end_date, farmer_count, output_dir):
    """Run a simulation scenario"""
    click.echo(f"Running {scenario} scenario...")
    
    # Update configuration
    global SIMULATION_START_DATE, SIMULATION_END_DATE, FARMER_COUNT, OUTPUT_DIRECTORY
    SIMULATION_START_DATE = start_date
    SIMULATION_END_DATE = end_date
    FARMER_COUNT = farmer_count
    OUTPUT_DIRECTORY = output_dir
    
    # Run selected scenario
    if scenario == 'baseline':
        results = run_baseline_scenario()
    elif scenario == 'climate_change':
        results = run_climate_change_scenario()
    else:
        results = run_technology_adoption_scenario()
    
    # Calculate and display summary
    total_production = sum(results[SIMULATION_END_DATE][region]['production']
                          for region in DISTRICTS)
    average_price = sum(results[SIMULATION_END_DATE][region]['market_price']
                       for region in DISTRICTS) / len(DISTRICTS)
    average_risk = sum((results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'] +
                       results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']) / 2
                      for region in DISTRICTS) / len(DISTRICTS)
    
    click.echo("\nSimulation Results:")
    click.echo("==================")
    click.echo(f"Total Production: {total_production:.2f} tons")
    click.echo(f"Average Price: {average_price:.2f} BDT/ton")
    click.echo(f"Average Risk: {average_risk:.2%}")
    
    # Save summary to file
    summary = {
        'scenario': scenario,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat(),
        'farmer_count': farmer_count,
        'total_production': total_production,
        'average_price': average_price,
        'average_risk': average_risk
    }
    
    output_path = Path(output_dir) / scenario / 'summary.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4)
    
    click.echo(f"\nResults saved to: {output_path}")

@cli.command()
@click.option('--start-date', type=click.DateTime(), default=SIMULATION_START_DATE,
              help='Simulation start date')
@click.option('--end-date', type=click.DateTime(), default=SIMULATION_END_DATE,
              help='Simulation end date')
@click.option('--farmer-count', type=int, default=FARMER_COUNT,
              help='Number of farmers to simulate')
@click.option('--output-dir', type=click.Path(), default=OUTPUT_DIRECTORY,
              help='Output directory for results')
def run_all_scenarios(start_date, end_date, farmer_count, output_dir):
    """Run all simulation scenarios and compare results"""
    click.echo("Running all scenarios...")
    
    # Update configuration
    global SIMULATION_START_DATE, SIMULATION_END_DATE, FARMER_COUNT, OUTPUT_DIRECTORY
    SIMULATION_START_DATE = start_date
    SIMULATION_END_DATE = end_date
    FARMER_COUNT = farmer_count
    OUTPUT_DIRECTORY = output_dir
    
    # Run all scenarios
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
    
    # Display comparison
    click.echo("\nScenario Comparison Results:")
    click.echo("============================")
    for scenario, metrics in comparison.items():
        click.echo(f"\n{scenario.upper()} SCENARIO:")
        click.echo(f"Total Production: {metrics['total_production']:.2f} tons")
        click.echo(f"Average Price: {metrics['average_price']:.2f} BDT/ton")
        click.echo(f"Average Risk: {metrics['average_risk']:.2%}")
    
    # Save comparison to file
    output_path = Path(output_dir) / 'scenario_comparison.json'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(comparison, f, indent=4)
    
    click.echo(f"\nComparison results saved to: {output_path}")

@cli.command()
def start_api():
    """Start the FastAPI server"""
    click.echo("Starting API server...")
    os.system("python scripts/run_api.py")

if __name__ == '__main__':
    cli() 