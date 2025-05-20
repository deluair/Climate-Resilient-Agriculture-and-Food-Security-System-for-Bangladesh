from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging
from .database.session import get_session
from .database.repository import SimulationRepository
from .data_generator import DataGenerator
from .utils.serialization import serialize_results

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
        self.session = next(get_session())
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
    
    def _generate_regions(self) -> List:
        """Generate regions and store in database, returning ORM objects."""
        regions = self.data_generator.generate_regions()
        db_regions = []
        for region in regions:
            db_region = self.repository.create_region(self.simulation.id, region)
            db_regions.append(db_region)
        return db_regions
    
    def _generate_farmers(self) -> List[Dict]:
        """Generate farmers and store in database"""
        farmers = self.data_generator.generate_farmer_data()
        for farmer in farmers:
            self.repository.create_farmer(self.simulation.id, farmer)
        return farmers
    
    def _generate_policies(self) -> List[Dict]:
        """Generate policies and store in database"""
        policies = self.data_generator.generate_policy_data()
        for policy in policies:
            self.repository.create_policy(self.simulation.id, policy)
        return policies
    
    def step(self) -> Dict:
        """Advance simulation by one time step"""
        if self.current_date >= self.end_date:
            return None
        
        climate_data_batch = []
        production_data_batch = []
        region_step_data = []
        
        for region in self.regions:
            # Generate climate data
            climate_data_records = self.data_generator.generate_climate_data(
                self.current_date, self.end_date
            )
            # Assume temperature and rainfall are always present in the two records
            temperature = None
            rainfall = None
            for record in climate_data_records:
                record['region_id'] = region.id
                climate_data_batch.append(record)
                if record['data_type'] == 'temperature':
                    temperature = record['value']
                elif record['data_type'] == 'rainfall':
                    rainfall = record['value']
            # Generate production data
            production_data = self.data_generator.calculate_production(
                region, self.current_date, self.scenario_type
            )
            production_data['region_id'] = region.id
            production_data_batch.append(production_data)
            crop_yield = production_data['yield_per_hectare']
            # Attach all info for serialization
            region_step_data.append({
                'id': region.id,
                'district': region.district,
                'upazila': region.upazila,
                'union': region.union,
                'latitude': region.latitude,
                'longitude': region.longitude,
                'elevation': region.elevation,
                'agro_ecological_zone': region.agro_ecological_zone,
                'temperature': temperature,
                'rainfall': rainfall,
                'crop_yield': crop_yield
            })
        # Batch insert climate data
        if climate_data_batch:
            self.repository.batch_create_climate_data(climate_data_batch)
        # Batch insert production data
        if production_data_batch:
            self.repository.batch_create_production_data(production_data_batch)
        # Update current date
        self.current_date += timedelta(days=1)
        return {
            'date': self.current_date,
            'regions': region_step_data
        }
    
    def run(self) -> Dict:
        """Run the complete simulation"""
        results = []
        while self.current_date < self.end_date:
            step_result = self.step()
            if step_result:
                results.append(step_result)
        
        # Serialize results before storing
        serialized_results = serialize_results(results)
        
        # Store final results
        self.repository.update_simulation_results(self.simulation.id, serialized_results)
        
        logger.info(f"Completed {self.scenario_type} simulation")
        return {
            'simulation_id': self.simulation.id,
            'results': serialized_results
        }
    
    def get_results(self) -> Dict:
        """Get simulation results from database"""
        return self.repository.get_simulation(self.simulation.id).results
    
    def cleanup(self):
        """Clean up resources"""
        self.session.close() 