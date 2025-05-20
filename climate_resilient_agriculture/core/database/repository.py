from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from .models import (
    Simulation, Region, Farmer, Policy,
    ClimateData, ProductionData
)

class SimulationRepository:
    """Repository for handling simulation data operations"""
    
    def __init__(self, session: Session):
        self.session = session
    
    def create_simulation(self, scenario_type: str, start_date: datetime,
                         end_date: datetime, parameters: Dict) -> Simulation:
        """Create a new simulation record"""
        simulation = Simulation(
            scenario_type=scenario_type,
            start_date=start_date,
            end_date=end_date,
            parameters=parameters
        )
        self.session.add(simulation)
        self.session.commit()
        return simulation
    
    def get_simulation(self, simulation_id: int) -> Optional[Simulation]:
        """Get a simulation by ID"""
        return self.session.query(Simulation).filter_by(id=simulation_id).first()
    
    def get_all_simulations(self) -> List[Simulation]:
        """Get all simulations"""
        return self.session.query(Simulation).all()
    
    def update_simulation_results(self, simulation_id: int, results: Dict) -> Simulation:
        """Update simulation results"""
        simulation = self.get_simulation(simulation_id)
        if simulation:
            simulation.results = results
            self.session.commit()
        return simulation
    
    def create_region(self, simulation_id: int, region_data: Dict) -> Region:
        """Create a new region record"""
        region = Region(
            simulation_id=simulation_id,
            **region_data
        )
        self.session.add(region)
        self.session.commit()
        return region
    
    def create_farmer(self, simulation_id: int, farmer_data: Dict) -> Farmer:
        """Create a new farmer record"""
        farmer = Farmer(
            simulation_id=simulation_id,
            **farmer_data
        )
        self.session.add(farmer)
        self.session.commit()
        return farmer
    
    def create_policy(self, simulation_id: int, policy_data: Dict) -> Policy:
        """Create a new policy record"""
        policy = Policy(
            simulation_id=simulation_id,
            **policy_data
        )
        self.session.add(policy)
        self.session.commit()
        return policy
    
    def create_climate_data(self, region_id: int, climate_data: Dict) -> ClimateData:
        """Create new climate data record"""
        data = ClimateData(
            region_id=region_id,
            **climate_data
        )
        self.session.add(data)
        self.session.commit()
        return data
    
    def create_production_data(self, region_id: int, production_data: Dict) -> ProductionData:
        """Create new production data record"""
        data = ProductionData(
            region_id=region_id,
            **production_data
        )
        self.session.add(data)
        self.session.commit()
        return data
    
    def get_simulation_regions(self, simulation_id: int) -> List[Region]:
        """Get all regions for a simulation"""
        return self.session.query(Region).filter_by(simulation_id=simulation_id).all()
    
    def get_simulation_farmers(self, simulation_id: int) -> List[Farmer]:
        """Get all farmers for a simulation"""
        return self.session.query(Farmer).filter_by(simulation_id=simulation_id).all()
    
    def get_simulation_policies(self, simulation_id: int) -> List[Policy]:
        """Get all policies for a simulation"""
        return self.session.query(Policy).filter_by(simulation_id=simulation_id).all()
    
    def get_region_climate_data(self, region_id: int,
                              start_date: datetime,
                              end_date: datetime) -> List[ClimateData]:
        """Get climate data for a region within a date range"""
        return self.session.query(ClimateData).filter(
            ClimateData.region_id == region_id,
            ClimateData.timestamp >= start_date,
            ClimateData.timestamp <= end_date
        ).all()
    
    def get_region_production_data(self, region_id: int,
                                 start_date: datetime,
                                 end_date: datetime) -> List[ProductionData]:
        """Get production data for a region within a date range"""
        return self.session.query(ProductionData).filter(
            ProductionData.region_id == region_id,
            ProductionData.timestamp >= start_date,
            ProductionData.timestamp <= end_date
        ).all()
    
    def delete_simulation(self, simulation_id: int) -> bool:
        """Delete a simulation and all related data"""
        simulation = self.get_simulation(simulation_id)
        if simulation:
            self.session.delete(simulation)
            self.session.commit()
            return True
        return False 