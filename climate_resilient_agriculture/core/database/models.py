from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Simulation(Base):
    """Model for storing simulation runs"""
    __tablename__ = 'simulations'
    
    id = Column(Integer, primary_key=True)
    scenario_type = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    parameters = Column(JSON)
    results = Column(JSON)
    
    # Relationships
    regions = relationship("Region", back_populates="simulation")
    farmers = relationship("Farmer", back_populates="simulation")
    policies = relationship("Policy", back_populates="simulation")

class Region(Base):
    """Model for storing region data"""
    __tablename__ = 'regions'
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    district = Column(String, nullable=False)
    upazila = Column(String)
    union = Column(String)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    elevation = Column(Float)
    agro_ecological_zone = Column(String)
    
    # Relationships
    simulation = relationship("Simulation", back_populates="regions")
    climate_data = relationship("ClimateData", back_populates="region")
    production_data = relationship("ProductionData", back_populates="region")

class Farmer(Base):
    """Model for storing farmer data"""
    __tablename__ = 'farmers'
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    farmer_id = Column(String, nullable=False)
    region_id = Column(Integer, ForeignKey('regions.id'))
    land_holding_size = Column(Float, nullable=False)
    farming_experience = Column(Integer)
    crops_grown = Column(JSON)
    irrigation_type = Column(String)
    technology_adoption_level = Column(Float)
    risk_tolerance = Column(Float)
    access_to_credit = Column(Boolean)
    access_to_insurance = Column(Boolean)
    
    # Relationships
    simulation = relationship("Simulation", back_populates="farmers")
    region = relationship("Region")

class Policy(Base):
    """Model for storing policy data"""
    __tablename__ = 'policies'
    
    id = Column(Integer, primary_key=True)
    simulation_id = Column(Integer, ForeignKey('simulations.id'))
    policy_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    target_sector = Column(String, nullable=False)
    budget_allocation = Column(Float)
    implementation_status = Column(String)
    success_metrics = Column(JSON)
    
    # Relationships
    simulation = relationship("Simulation", back_populates="policies")

class ClimateData(Base):
    """Model for storing climate data"""
    __tablename__ = 'climate_data'
    
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    timestamp = Column(DateTime, nullable=False)
    data_type = Column(String, nullable=False)  # temperature, rainfall, etc.
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    source = Column(String)
    quality_score = Column(Float)
    confidence_interval = Column(JSON)
    
    # Relationships
    region = relationship("Region", back_populates="climate_data")

class ProductionData(Base):
    """Model for storing production data"""
    __tablename__ = 'production_data'
    
    id = Column(Integer, primary_key=True)
    region_id = Column(Integer, ForeignKey('regions.id'))
    timestamp = Column(DateTime, nullable=False)
    crop_type = Column(String, nullable=False)
    area_hectares = Column(Float)
    yield_per_hectare = Column(Float)
    total_production = Column(Float)
    production_cost = Column(Float)
    market_price = Column(Float)
    
    # Relationships
    region = relationship("Region", back_populates="production_data") 