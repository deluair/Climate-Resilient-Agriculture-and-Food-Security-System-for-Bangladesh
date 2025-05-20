from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from ..models.base import (
    Location,
    ClimateData,
    AgriculturalProduction,
    FarmerProfile,
    MarketData,
    Policy,
    Infrastructure
)

class SimulationEngine:
    """Core simulation engine for climate-resilient agriculture system"""
    
    def __init__(self, start_date: datetime, end_date: datetime, time_step: timedelta):
        self.start_date = start_date
        self.end_date = end_date
        self.time_step = time_step
        self.current_date = start_date
        self.regions: Dict[str, Location] = {}
        self.farmers: Dict[str, FarmerProfile] = {}
        self.infrastructure: Dict[str, Infrastructure] = {}
        self.policies: Dict[str, Policy] = {}
        self.climate_data: Dict[str, List[ClimateData]] = {}
        self.market_data: Dict[str, List[MarketData]] = {}
        self.production_data: Dict[str, List[AgriculturalProduction]] = {}
        
    def add_region(self, location: Location) -> None:
        """Add a region to the simulation"""
        self.regions[location.district] = location
        
    def add_farmer(self, farmer: FarmerProfile) -> None:
        """Add a farmer to the simulation"""
        self.farmers[farmer.farmer_id] = farmer
        
    def add_infrastructure(self, infrastructure: Infrastructure) -> None:
        """Add infrastructure to the simulation"""
        self.infrastructure[infrastructure.infrastructure_id] = infrastructure
        
    def add_policy(self, policy: Policy) -> None:
        """Add a policy to the simulation"""
        self.policies[policy.policy_id] = policy
        
    def simulate_climate_impact(self, region: str) -> Dict[str, float]:
        """Simulate climate impact on a region"""
        # This is a simplified model - in reality, this would use complex climate models
        base_temp = 25.0  # Base temperature in Celsius
        base_rainfall = 2000.0  # Base annual rainfall in mm
        
        # Simulate temperature increase
        temp_increase = np.random.normal(0.5, 0.2)  # Mean increase of 0.5°C with some variation
        rainfall_change = np.random.normal(-100, 50)  # Mean decrease of 100mm with variation
        
        return {
            "temperature_change": temp_increase,
            "rainfall_change": rainfall_change,
            "drought_risk": max(0, min(1, (rainfall_change + 100) / 200)),
            "flood_risk": max(0, min(1, (-rainfall_change + 100) / 200))
        }
        
    def simulate_crop_yield(self, farmer: FarmerProfile, climate_impact: Dict[str, float]) -> float:
        """Simulate crop yield based on farmer profile and climate impact"""
        base_yield = 4.0  # Base yield in tons per hectare
        
        # Factors affecting yield
        technology_factor = farmer.technology_adoption_level
        experience_factor = min(1.0, farmer.farming_experience / 20)  # Normalize experience
        climate_factor = 1.0 - (climate_impact["drought_risk"] + climate_impact["flood_risk"]) / 2
        
        # Calculate final yield
        yield_factor = (technology_factor * 0.4 + experience_factor * 0.3 + climate_factor * 0.3)
        final_yield = base_yield * yield_factor
        
        return max(0, final_yield)  # Ensure non-negative yield
        
    def simulate_market_prices(self, production: float, demand: float) -> float:
        """Simulate market prices based on supply and demand"""
        base_price = 1000  # Base price in BDT per ton
        supply_demand_ratio = production / demand
        
        # Price adjustment based on supply-demand ratio
        price_adjustment = 1.0 / (supply_demand_ratio + 0.1)  # Add 0.1 to prevent division by zero
        final_price = base_price * price_adjustment
        
        return final_price
        
    def run_simulation_step(self) -> Dict[str, Dict[str, float]]:
        """Run one step of the simulation"""
        results = {}
        
        for region_id, region in self.regions.items():
            # Simulate climate impact
            climate_impact = self.simulate_climate_impact(region_id)
            
            # Simulate agricultural production
            region_production = 0
            for farmer_id, farmer in self.farmers.items():
                if farmer.location.district == region_id:
                    yield_per_hectare = self.simulate_crop_yield(farmer, climate_impact)
                    production = yield_per_hectare * farmer.land_holding_size
                    region_production += production
            
            # Simulate market prices
            demand = region_production * 1.1  # Assume 10% more demand than production
            market_price = self.simulate_market_prices(region_production, demand)
            
            results[region_id] = {
                "production": region_production,
                "market_price": market_price,
                "climate_impact": climate_impact
            }
        
        self.current_date += self.time_step
        return results
        
    def run_full_simulation(self) -> Dict[datetime, Dict[str, Dict[str, float]]]:
        """Run the full simulation from start to end date"""
        results = {}
        
        while self.current_date <= self.end_date:
            step_results = self.run_simulation_step()
            results[self.current_date] = step_results
            
        return results 