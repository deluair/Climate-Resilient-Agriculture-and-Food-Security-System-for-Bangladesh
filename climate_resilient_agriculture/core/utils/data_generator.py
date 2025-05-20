from datetime import datetime, timedelta
import numpy as np
from typing import Dict, List, Tuple
from ..models.base import (
    Location,
    ClimateData,
    AgriculturalProduction,
    FarmerProfile,
    MarketData,
    Policy,
    Infrastructure
)

class DataGenerator:
    """Utility class for generating realistic simulation data"""
    
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        
        # Bangladesh-specific constants
        self.DISTRICTS = [
            "Dhaka", "Chittagong", "Khulna", "Rajshahi", "Barishal",
            "Sylhet", "Rangpur", "Mymensingh", "Comilla", "Noakhali"
        ]
        
        self.AGRO_ECOLOGICAL_ZONES = [
            "Coastal Zone", "Haor Basin", "Barind Tract",
            "Chittagong Hill Tracts", "Floodplains", "Char Islands"
        ]
        
        self.CROPS = [
            "Rice", "Wheat", "Maize", "Potato", "Jute",
            "Sugarcane", "Vegetables", "Fruits"
        ]
        
        self.IRRIGATION_TYPES = [
            "Surface Water", "Groundwater", "Rain-fed",
            "Solar-powered", "Drip", "Sprinkler"
        ]
        
    def generate_location(self, district: str = None) -> Location:
        """Generate a realistic location in Bangladesh"""
        if district is None:
            district = np.random.choice(self.DISTRICTS)
            
        # Generate realistic coordinates for the district
        coordinates = {
            "Dhaka": (23.8103, 90.4125),
            "Chittagong": (22.3419, 91.8132),
            "Khulna": (22.8456, 89.5403),
            "Rajshahi": (24.3745, 88.6042),
            "Barishal": (22.7010, 90.3535),
            "Sylhet": (24.8949, 91.8687),
            "Rangpur": (25.7439, 89.2752),
            "Mymensingh": (24.7471, 90.4203),
            "Comilla": (23.4607, 91.1809),
            "Noakhali": (22.8333, 91.1000)
        }
        
        lat, lon = coordinates[district]
        # Add some random variation
        lat += np.random.normal(0, 0.1)
        lon += np.random.normal(0, 0.1)
        
        return Location(
            district=district,
            upazila=f"{district}_Upazila_{np.random.randint(1, 10)}",
            union=f"Union_{np.random.randint(1, 20)}",
            latitude=lat,
            longitude=lon,
            elevation=np.random.uniform(1, 100),
            agro_ecological_zone=np.random.choice(self.AGRO_ECOLOGICAL_ZONES)
        )
        
    def generate_farmer_profile(self, location: Location = None) -> FarmerProfile:
        """Generate a realistic farmer profile"""
        if location is None:
            location = self.generate_location()
            
        return FarmerProfile(
            farmer_id=f"F{np.random.randint(10000, 99999)}",
            location=location,
            land_holding_size=np.random.lognormal(0, 0.5),  # Most farmers have small holdings
            farming_experience=np.random.randint(1, 40),
            crops_grown=np.random.choice(self.CROPS, size=np.random.randint(1, 4), replace=False).tolist(),
            irrigation_type=np.random.choice(self.IRRIGATION_TYPES),
            technology_adoption_level=np.random.beta(2, 5),  # Most farmers have low adoption
            risk_tolerance=np.random.beta(2, 2),
            access_to_credit=np.random.random() > 0.7,  # 30% have access to credit
            access_to_insurance=np.random.random() > 0.9  # 10% have access to insurance
        )
        
    def generate_climate_data(self, location: Location, start_date: datetime, end_date: datetime) -> List[ClimateData]:
        """Generate realistic climate data for a location"""
        climate_data = []
        current_date = start_date
        
        while current_date <= end_date:
            # Generate temperature data
            base_temp = 25.0  # Base temperature in Celsius
            seasonal_variation = 10 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
            temp = base_temp + seasonal_variation + np.random.normal(0, 2)
            
            climate_data.append(ClimateData(
                timestamp=current_date,
                value=temp,
                unit="Celsius",
                data_type="temperature",
                source="Simulated",
                quality_score=np.random.uniform(0.8, 1.0),
                confidence_interval={"lower": temp - 1, "upper": temp + 1}
            ))
            
            # Generate rainfall data
            if 5 <= current_date.month <= 9:  # Monsoon season
                rainfall = np.random.exponential(50)  # Higher rainfall during monsoon
            else:
                rainfall = np.random.exponential(10)  # Lower rainfall in other seasons
                
            climate_data.append(ClimateData(
                timestamp=current_date,
                value=rainfall,
                unit="mm",
                data_type="rainfall",
                source="Simulated",
                quality_score=np.random.uniform(0.8, 1.0),
                confidence_interval={"lower": rainfall * 0.8, "upper": rainfall * 1.2}
            ))
            
            current_date += timedelta(days=1)
            
        return climate_data
        
    def generate_market_data(self, location: Location, start_date: datetime, end_date: datetime) -> List[MarketData]:
        """Generate realistic market data"""
        market_data = []
        current_date = start_date
        
        while current_date <= end_date:
            for crop in self.CROPS:
                # Generate base price with seasonal variation
                base_price = 1000  # Base price in BDT per ton
                seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * current_date.timetuple().tm_yday / 365)
                price = base_price * seasonal_factor * np.random.lognormal(0, 0.1)
                
                # Generate volume
                volume = np.random.lognormal(5, 1)  # Volume in tons
                
                market_data.append(MarketData(
                    market_id=f"M{np.random.randint(1000, 9999)}",
                    location=location,
                    commodity_type=crop,
                    price=price,
                    volume=volume,
                    timestamp=current_date,
                    source="Simulated"
                ))
                
            current_date += timedelta(days=7)  # Weekly market data
            
        return market_data
        
    def generate_infrastructure(self, location: Location) -> Infrastructure:
        """Generate realistic infrastructure data"""
        infrastructure_types = ["storage", "irrigation", "transportation"]
        infrastructure_type = np.random.choice(infrastructure_types)
        
        return Infrastructure(
            infrastructure_id=f"I{np.random.randint(10000, 99999)}",
            type=infrastructure_type,
            location=location,
            capacity=np.random.lognormal(5, 1),
            operational_status=np.random.choice(["operational", "maintenance", "under_construction"]),
            maintenance_status=np.random.choice(["good", "fair", "poor"]),
            last_inspection_date=datetime.now() - timedelta(days=np.random.randint(0, 365)),
            next_maintenance_date=datetime.now() + timedelta(days=np.random.randint(30, 365))
        )
        
    def generate_policy(self) -> Policy:
        """Generate realistic policy data"""
        policy_types = [
            "subsidy", "credit", "insurance", "technology_adoption",
            "infrastructure_development", "research_development"
        ]
        
        return Policy(
            policy_id=f"P{np.random.randint(10000, 99999)}",
            name=f"Policy_{np.random.randint(1, 100)}",
            description="Simulated policy for agricultural development",
            start_date=datetime.now(),
            end_date=datetime.now() + timedelta(days=np.random.randint(365, 3650)),
            target_sector=np.random.choice(policy_types),
            budget_allocation=np.random.lognormal(10, 1),
            implementation_status=np.random.choice(["planned", "ongoing", "completed"]),
            success_metrics={
                "adoption_rate": np.random.uniform(0, 1),
                "cost_effectiveness": np.random.uniform(0, 1),
                "farmer_satisfaction": np.random.uniform(0, 1)
            }
        ) 