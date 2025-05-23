import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from typing import Dict, List
from pathlib import Path
import folium
from folium.plugins import HeatMap

class SimulationVisualizer:
    """Visualizes simulation results"""
    
    def __init__(self):
        """Initialize the visualizer"""
        plt.style.use('default')  # Use default style instead of seaborn
    
    def generate_comparison_plots(self, results: Dict, output_dir: Path):
        """Generate comparison plots for different scenarios"""
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Plot temperature trends
        self._plot_temperature_trends(results, output_dir)
        
        # Plot rainfall patterns
        self._plot_rainfall_patterns(results, output_dir)
        
        # Plot crop yields
        self._plot_crop_yields(results, output_dir)
        
        plt.close('all')
    
    def _plot_temperature_trends(self, results: Dict, output_dir: Path):
        """Plot temperature trends for different scenarios"""
        plt.figure(figsize=(12, 6))
        
        for scenario, data in results.items():
            dates = [pd.to_datetime(r['date']) for r in data['results']]
            temps = [r['regions'][0]['temperature'] for r in data['results']]
            plt.plot(dates, temps, label=scenario)
        
        plt.title('Temperature Trends Across Scenarios')
        plt.xlabel('Date')
        plt.ylabel('Temperature (°C)')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / 'temperature_trends.png')
        plt.close()
    
    def _plot_rainfall_patterns(self, results: Dict, output_dir: Path):
        """Plot rainfall patterns for different scenarios"""
        plt.figure(figsize=(12, 6))
        
        for scenario, data in results.items():
            dates = [pd.to_datetime(r['date']) for r in data['results']]
            rainfall = [r['regions'][0]['rainfall'] for r in data['results']]
            plt.plot(dates, rainfall, label=scenario)
        
        plt.title('Rainfall Patterns Across Scenarios')
        plt.xlabel('Date')
        plt.ylabel('Rainfall (mm)')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / 'rainfall_patterns.png')
        plt.close()
    
    def _plot_crop_yields(self, results: Dict, output_dir: Path):
        """Plot crop yields for different scenarios"""
        plt.figure(figsize=(12, 6))
        
        for scenario, data in results.items():
            dates = [pd.to_datetime(r['date']) for r in data['results']]
            yields = [r['regions'][0]['crop_yield'] for r in data['results']]
            plt.plot(dates, yields, label=scenario)
        
        plt.title('Crop Yields Across Scenarios')
        plt.xlabel('Date')
        plt.ylabel('Yield (tons/hectare)')
        plt.legend()
        plt.grid(True)
        plt.savefig(output_dir / 'crop_yields.png')
        plt.close()
        
    def plot_climate_impact(self, climate_data: Dict[str, List[Dict[str, float]]], 
                          save_path: str = None) -> None:
        """Plot climate impact over time"""
        plt.figure(figsize=(12, 6))
        
        for region, data in climate_data.items():
            dates = [d for d in data.keys()]
            temp_changes = [d['climate_impact']['temperature_change'] for d in data.values()]
            rainfall_changes = [d['climate_impact']['rainfall_change'] for d in data.values()]
            
            plt.subplot(2, 1, 1)
            plt.plot(dates, temp_changes, label=region)
            plt.title('Temperature Change Over Time')
            plt.ylabel('Temperature Change (°C)')
            plt.legend()
            
            plt.subplot(2, 1, 2)
            plt.plot(dates, rainfall_changes, label=region)
            plt.title('Rainfall Change Over Time')
            plt.ylabel('Rainfall Change (mm)')
            plt.legend()
            
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
    def plot_production_trends(self, production_data: Dict[str, List[Dict[str, float]]],
                             save_path: str = None) -> None:
        """Plot agricultural production trends"""
        plt.figure(figsize=(12, 6))
        
        for region, data in production_data.items():
            dates = [d for d in data.keys()]
            production = [d['production'] for d in data.values()]
            prices = [d['market_price'] for d in data.values()]
            
            plt.subplot(2, 1, 1)
            plt.plot(dates, production, label=region)
            plt.title('Agricultural Production Over Time')
            plt.ylabel('Production (tons)')
            plt.legend()
            
            plt.subplot(2, 1, 2)
            plt.plot(dates, prices, label=region)
            plt.title('Market Prices Over Time')
            plt.ylabel('Price (BDT/ton)')
            plt.legend()
            
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
    def create_risk_map(self, locations: Dict[str, Dict[str, float]], 
                       save_path: str = None) -> None:
        """Create a heat map of climate risks"""
        # Create a map centered on Bangladesh
        m = folium.Map(location=[23.6850, 90.3563], zoom_start=7)
        
        # Add risk heatmap
        risk_data = []
        for location, data in locations.items():
            risk = (data['drought_risk'] + data['flood_risk']) / 2
            risk_data.append([data['latitude'], data['longitude'], risk])
            
        HeatMap(risk_data).add_to(m)
        
        if save_path:
            m.save(save_path)
        return m
        
    def plot_farmer_distribution(self, farmers: List[Dict], save_path: str = None) -> None:
        """Plot distribution of farmer characteristics"""
        plt.figure(figsize=(15, 10))
        
        # Land holding size distribution
        plt.subplot(2, 2, 1)
        land_sizes = [f['land_holding_size'] for f in farmers]
        plt.hist(land_sizes, bins=30)
        plt.title('Distribution of Land Holding Sizes')
        plt.xlabel('Land Size (hectares)')
        
        # Technology adoption level
        plt.subplot(2, 2, 2)
        tech_levels = [f['technology_adoption_level'] for f in farmers]
        plt.hist(tech_levels, bins=30)
        plt.title('Distribution of Technology Adoption Levels')
        plt.xlabel('Adoption Level')
        
        # Farming experience
        plt.subplot(2, 2, 3)
        experience = [f['farming_experience'] for f in farmers]
        plt.hist(experience, bins=30)
        plt.title('Distribution of Farming Experience')
        plt.xlabel('Years of Experience')
        
        # Risk tolerance
        plt.subplot(2, 2, 4)
        risk_tolerance = [f['risk_tolerance'] for f in farmers]
        plt.hist(risk_tolerance, bins=30)
        plt.title('Distribution of Risk Tolerance')
        plt.xlabel('Risk Tolerance Level')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
    def plot_policy_impact(self, policy_data: Dict[str, Dict[str, float]], 
                          save_path: str = None) -> None:
        """Plot impact of different policies"""
        plt.figure(figsize=(12, 6))
        
        metrics = ['adoption_rate', 'cost_effectiveness', 'farmer_satisfaction']
        policy_types = list(policy_data.keys())
        
        x = np.arange(len(policy_types))
        width = 0.25
        
        for i, metric in enumerate(metrics):
            values = [policy_data[policy][metric] for policy in policy_types]
            plt.bar(x + i*width, values, width, label=metric)
            
        plt.xlabel('Policy Type')
        plt.ylabel('Score')
        plt.title('Policy Impact Analysis')
        plt.xticks(x + width, policy_types, rotation=45)
        plt.legend()
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
    def create_dashboard(self, simulation_results: Dict, save_path: str = None) -> None:
        """Create a comprehensive dashboard of simulation results"""
        fig = plt.figure(figsize=(20, 15))
        
        # Climate Impact
        plt.subplot(3, 2, 1)
        self._plot_climate_summary(simulation_results['climate_data'])
        
        # Production Trends
        plt.subplot(3, 2, 2)
        self._plot_production_summary(simulation_results['production_data'])
        
        # Market Prices
        plt.subplot(3, 2, 3)
        self._plot_market_summary(simulation_results['market_data'])
        
        # Policy Impact
        plt.subplot(3, 2, 4)
        self._plot_policy_summary(simulation_results['policy_data'])
        
        # Farmer Distribution
        plt.subplot(3, 2, 5)
        self._plot_farmer_summary(simulation_results['farmer_data'])
        
        # Risk Assessment
        plt.subplot(3, 2, 6)
        self._plot_risk_summary(simulation_results['risk_data'])
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path)
        plt.show()
        
    def _plot_climate_summary(self, climate_data: Dict) -> None:
        """Helper method to plot climate summary"""
        # Implementation details for climate summary plot
        pass
        
    def _plot_production_summary(self, production_data: Dict) -> None:
        """Helper method to plot production summary"""
        # Implementation details for production summary plot
        pass
        
    def _plot_market_summary(self, market_data: Dict) -> None:
        """Helper method to plot market summary"""
        # Implementation details for market summary plot
        pass
        
    def _plot_policy_summary(self, policy_data: Dict) -> None:
        """Helper method to plot policy summary"""
        # Implementation details for policy summary plot
        pass
        
    def _plot_farmer_summary(self, farmer_data: Dict) -> None:
        """Helper method to plot farmer summary"""
        # Implementation details for farmer summary plot
        pass
        
    def _plot_risk_summary(self, risk_data: Dict) -> None:
        """Helper method to plot risk summary"""
        # Implementation details for risk summary plot
        pass 