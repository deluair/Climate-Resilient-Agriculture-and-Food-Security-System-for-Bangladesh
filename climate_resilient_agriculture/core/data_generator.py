import random
from datetime import datetime, timedelta
from typing import Dict, List, Any
from climate_resilient_agriculture.config.simulation_config import DISTRICTS, AGRO_ECOLOGICAL_ZONES

class DataGenerator:
    """Generates data for climate-resilient agriculture simulation."""
    
    def __init__(self):
        """Initialize the data generator."""
        self.districts = [
            "Dhaka", "Chittagong", "Rajshahi", "Khulna", "Barishal",
            "Sylhet", "Rangpur", "Mymensingh", "Comilla", "Noakhali"
        ]
        
        self.crops = [
            "rice", "wheat", "maize", "jute", "potato",
            "sugarcane", "pulses", "oilseeds", "vegetables", "fruits"
        ]
        
        self.policies = [
            "irrigation_development",
            "crop_insurance",
            "climate_smart_agriculture",
            "market_access",
            "research_development"
        ]
    
    def generate_climate_data(self, start_date: datetime, end_date: datetime) -> list:
        """Generate climate data records for a region and time period, matching ClimateData model fields."""
        # Pre-generate random values for efficiency
        temp_value = round(random.uniform(20.0, 35.0), 2)
        temp_ci = [round(random.uniform(-0.5, 0.5), 2), round(random.uniform(-0.5, 0.5), 2)]
        rain_value = round(random.uniform(0, 50), 2)
        rain_ci = [round(random.uniform(-5, 5), 2), round(random.uniform(-5, 5), 2)]
        
        records = [
            {
                'timestamp': start_date,
                'data_type': 'temperature',
                'value': temp_value,
                'unit': 'C',
                'source': 'simulated',
                'quality_score': 1.0,
                'confidence_interval': temp_ci
            },
            {
                'timestamp': start_date,
                'data_type': 'rainfall',
                'value': rain_value,
                'unit': 'mm',
                'source': 'simulated',
                'quality_score': 1.0,
                'confidence_interval': rain_ci
            }
        ]
        return records
    
    def generate_farmer_data(self, num_farmers: int = 1000) -> List[Dict[str, Any]]:
        """Generate data for farmers, matching Farmer model fields."""
        farmers = []
        for i in range(num_farmers):
            farmer = {
                "farmer_id": f"F{i+1:04d}",
                "land_holding_size": round(random.uniform(0.5, 5.0), 2),  # hectares
                "farming_experience": random.randint(1, 40),
                "crops_grown": [random.choice(self.crops)],
                "irrigation_type": random.choice(["canal", "tube_well", "rainfed"]),
                "technology_adoption_level": round(random.uniform(0.0, 1.0), 2),
                "risk_tolerance": round(random.uniform(0.0, 1.0), 2),
                "access_to_credit": random.random() < 0.6,
                "access_to_insurance": random.random() < 0.5
            }
            farmers.append(farmer)
        return farmers
    
    def generate_crop_data(self) -> Dict[str, Dict[str, float]]:
        """Generate data for crops."""
        crop_data = {}
        for crop in self.crops:
            crop_data[crop] = {
                "base_yield": round(random.uniform(2.0, 5.0), 2),  # tons/hectare
                "price": round(random.uniform(20000, 50000), 2),  # BDT/ton
                "water_requirement": round(random.uniform(500, 2000), 2),  # mm/season
                "temperature_sensitivity": round(random.uniform(0.1, 0.3), 2),
                "flood_sensitivity": round(random.uniform(0.2, 0.5), 2),
                "drought_sensitivity": round(random.uniform(0.2, 0.5), 2)
            }
        return crop_data
    
    def generate_policy_data(self) -> Dict[str, Dict[str, Any]]:
        """Generate data for agricultural policies, matching Policy model fields."""
        policy_data = {}
        for i, policy in enumerate(self.policies):
            policy_data[policy] = {
                "policy_id": f"P{i+1:03d}",
                "name": policy.replace('_', ' ').title(),
                "description": f"Policy for {policy.replace('_', ' ')}.",
                "start_date": datetime(2020, 1, 1),
                "end_date": datetime(2025, 12, 31),
                "target_sector": random.choice(["crop", "infrastructure", "market", "technology"]),
                "budget_allocation": round(random.uniform(1000000, 5000000), 2),
                "implementation_status": random.choice(["planned", "ongoing", "completed"]),
                "success_metrics": {"effectiveness": round(random.uniform(0.3, 0.8), 2)}
            }
        return list(policy_data.values())
    
    def generate_regions(self) -> list:
        """Generate region data using DISTRICTS and AGRO_ECOLOGICAL_ZONES, matching Region model fields."""
        regions = []
        for i, district in enumerate(DISTRICTS):
            region = {
                'district': district,
                'upazila': f'Upazila-{i+1}',
                'union': f'Union-{i+1}',
                'latitude': 23.5 + i * 0.1,  # placeholder
                'longitude': 90.0 + i * 0.1,  # placeholder
                'elevation': 10.0 + i,        # placeholder
                'agro_ecological_zone': AGRO_ECOLOGICAL_ZONES[i % len(AGRO_ECOLOGICAL_ZONES)]
            }
            regions.append(region)
        return regions
    
    def generate_all_data(
        self,
        start_date: datetime,
        end_date: datetime,
        num_farmers: int = 1000
    ) -> Dict[str, Any]:
        """Generate all data needed for simulation."""
        return {
            "climate_data": self.generate_climate_data(start_date, end_date),
            "farmers": self.generate_farmer_data(num_farmers),
            "crop_data": self.generate_crop_data(),
            "policy_data": self.generate_policy_data()
        }
    
    def calculate_production(self, region, current_date, scenario_type) -> dict:
        """Calculate production data for a region and date, matching ProductionData model fields."""
        crop = random.choice(self.crops)
        area = round(random.uniform(1.0, 10.0), 2)
        yield_per_hectare = round(random.uniform(2.0, 5.0), 2)
        total_production = round(area * yield_per_hectare, 2)
        production_cost = round(random.uniform(10000, 50000), 2)
        market_price = round(random.uniform(20000, 50000), 2)
        return {
            'timestamp': current_date,
            'crop_type': crop,
            'area_hectares': area,
            'yield_per_hectare': yield_per_hectare,
            'total_production': total_production,
            'production_cost': production_cost,
            'market_price': market_price
        } 