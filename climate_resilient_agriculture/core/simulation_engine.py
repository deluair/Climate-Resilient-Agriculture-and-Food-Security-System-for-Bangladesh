from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from .database.session import get_session
from .database.repository import SimulationRepository
from .data_generator import DataGenerator
from .visualization import generate_visualizations

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimulationEngine:
    """Engine for running climate-resilient agriculture simulations"""
    
    def __init__(self, start_date: datetime, end_date: datetime,
                 scenario_type: str = "baseline", parameters: Optional[Dict] = None):
        self.start_date = start_date
        self.end_date = end_date
        self.scenario_type = scenario_type
        self.parameters = parameters or {}
        self.current_date = start_date
        self.data_generator = DataGenerator()
        self.session = get_session()
        self.repository = SimulationRepository(self.session)
        
        # Initialize simulation record
        self.simulation = self.repository.create_simulation(
            scenario_type=scenario_type,
            start_date=start_date,
            end_date=end_date,
            parameters=parameters
        )
        
        # Generate initial data
        self.regions = self._generate_regions()
        self.farmers = self._generate_farmers()
        self.policies = self._generate_policies()
        
        logger.info(f"Initialized simulation engine for {scenario_type} scenario")
    
    def _generate_regions(self) -> List[Dict]:
        """Generate regions and store in database"""
        regions = self.data_generator.generate_regions()
        for region in regions:
            self.repository.create_region(self.simulation.id, region)
        return regions
    
    def _generate_farmers(self) -> List[Dict]:
        """Generate farmers and store in database"""
        farmers = self.data_generator.generate_farmers()
        for farmer in farmers:
            self.repository.create_farmer(self.simulation.id, farmer)
        return farmers
    
    def _generate_policies(self) -> List[Dict]:
        """Generate policies and store in database"""
        policies = self.data_generator.generate_policies()
        for policy in policies:
            self.repository.create_policy(self.simulation.id, policy)
        return policies
    
    def step(self) -> Dict:
        """Advance simulation by one time step"""
        if self.current_date >= self.end_date:
            return None
        
        # Update climate data
        for region in self.regions:
            climate_data = self.data_generator.generate_climate_data(
                region, self.current_date, self.scenario_type
            )
            self.repository.create_climate_data(region['id'], climate_data)
        
        # Calculate production
        for region in self.regions:
            production_data = self.data_generator.calculate_production(
                region, self.current_date, self.scenario_type
            )
            self.repository.create_production_data(region['id'], production_data)
        
        # Update current date
        self.current_date += timedelta(days=1)
        
        return {
            'date': self.current_date,
            'regions': self.regions
        }
    
    def run(self) -> Dict:
        """Run the complete simulation"""
        results = []
        while self.current_date < self.end_date:
            step_result = self.step()
            if step_result:
                results.append(step_result)
        
        # Store final results
        self.repository.update_simulation_results(self.simulation.id, results)
        
        # Generate visualizations
        visualizations = generate_visualizations(results)
        
        logger.info(f"Completed {self.scenario_type} simulation")
        return {
            'simulation_id': self.simulation.id,
            'results': results,
            'visualizations': visualizations
        }
    
    def get_results(self) -> Dict:
        """Get simulation results from database"""
        return self.repository.get_simulation(self.simulation.id).results
    
    def cleanup(self):
        """Clean up resources"""
        self.session.close() 