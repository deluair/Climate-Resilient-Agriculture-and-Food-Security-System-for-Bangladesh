from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

class Location(BaseModel):
    """Represents a geographical location in Bangladesh"""
    district: str
    upazila: str
    union: Optional[str]
    latitude: float
    longitude: float
    elevation: float
    agro_ecological_zone: str

class TimeSeriesData(BaseModel):
    """Base class for time series data"""
    timestamp: datetime
    value: float
    unit: str
    confidence_interval: Optional[Dict[str, float]]

class ClimateData(TimeSeriesData):
    """Climate-related time series data"""
    data_type: str  # temperature, rainfall, humidity, etc.
    source: str
    quality_score: float = Field(ge=0.0, le=1.0)

class AgriculturalProduction(BaseModel):
    """Agricultural production data"""
    crop_type: str
    area_hectares: float
    yield_per_hectare: float
    total_production: float
    production_cost: float
    market_price: float
    season: str
    year: int

class FarmerProfile(BaseModel):
    """Farmer profile data"""
    farmer_id: str
    location: Location
    land_holding_size: float  # in hectares
    farming_experience: int  # in years
    crops_grown: List[str]
    irrigation_type: str
    technology_adoption_level: float = Field(ge=0.0, le=1.0)
    risk_tolerance: float = Field(ge=0.0, le=1.0)
    access_to_credit: bool
    access_to_insurance: bool

class MarketData(BaseModel):
    """Market-related data"""
    market_id: str
    location: Location
    commodity_type: str
    price: float
    volume: float
    timestamp: datetime
    source: str

class Policy(BaseModel):
    """Policy framework data"""
    policy_id: str
    name: str
    description: str
    start_date: datetime
    end_date: Optional[datetime]
    target_sector: str
    budget_allocation: float
    implementation_status: str
    success_metrics: Dict[str, float]

class Infrastructure(BaseModel):
    """Infrastructure data"""
    infrastructure_id: str
    type: str  # storage, irrigation, transportation, etc.
    location: Location
    capacity: float
    operational_status: str
    maintenance_status: str
    last_inspection_date: datetime
    next_maintenance_date: datetime 