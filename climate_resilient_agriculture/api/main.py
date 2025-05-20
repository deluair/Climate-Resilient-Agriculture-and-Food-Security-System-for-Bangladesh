from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
import json
from pathlib import Path
import sys
import os
import logging

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.simulation.engine import SimulationEngine
from core.utils.data_generator import DataGenerator
from analysis.visualization import SimulationVisualizer
from config.simulation_config import *
from core.database.session import get_session
from core.database.repository import SimulationRepository
from core.database.init_db import init_db

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Climate-Resilient Agriculture Simulation API",
    description="API for simulating climate-resilient agriculture scenarios in Bangladesh",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

class SimulationRequest(BaseModel):
    """Request model for simulation parameters"""
    start_date: datetime
    end_date: datetime
    scenario_type: str
    parameters: Optional[Dict] = None

class SimulationResponse(BaseModel):
    """Response model for simulation results"""
    simulation_id: int
    results: Dict
    visualizations: Dict

@app.get("/")
async def read_main():
    """Get API information"""
    return {
        "title": app.title,
        "version": app.version,
        "description": app.description
    }

@app.get("/scenarios")
async def get_scenarios():
    """Get available simulation scenarios"""
    return {
        "scenarios": [
            "baseline",
            "climate_change",
            "technology_adoption"
        ]
    }

@app.get("/simulations")
async def get_simulations():
    """Get all simulations"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        simulations = repository.get_all_simulations()
        return {
            "simulations": [
                {
                    "id": sim.id,
                    "scenario_type": sim.scenario_type,
                    "start_date": sim.start_date,
                    "end_date": sim.end_date,
                    "parameters": sim.parameters
                }
                for sim in simulations
            ]
        }
    finally:
        session.close()

@app.get("/simulations/{simulation_id}")
async def get_simulation(simulation_id: int):
    """Get a specific simulation"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        simulation = repository.get_simulation(simulation_id)
        if not simulation:
            raise HTTPException(status_code=404, detail="Simulation not found")
        
        return {
            "id": simulation.id,
            "scenario_type": simulation.scenario_type,
            "start_date": simulation.start_date,
            "end_date": simulation.end_date,
            "parameters": simulation.parameters,
            "results": simulation.results
        }
    finally:
        session.close()

@app.post("/simulate", response_model=SimulationResponse)
async def run_simulation(request: SimulationRequest):
    """Run a new simulation"""
    try:
        # Initialize simulation engine
        engine = SimulationEngine(
            start_date=request.start_date,
            end_date=request.end_date,
            scenario_type=request.scenario_type,
            parameters=request.parameters
        )
        
        # Run simulation
        result = engine.run()
        
        # Clean up
        engine.cleanup()
        
        return result
    except Exception as e:
        logger.error(f"Error running simulation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/simulations/{simulation_id}")
async def delete_simulation(simulation_id: int):
    """Delete a simulation"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        success = repository.delete_simulation(simulation_id)
        if not success:
            raise HTTPException(status_code=404, detail="Simulation not found")
        return {"message": "Simulation deleted successfully"}
    finally:
        session.close()

@app.get("/simulations/{simulation_id}/regions")
async def get_simulation_regions(simulation_id: int):
    """Get regions for a simulation"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        regions = repository.get_simulation_regions(simulation_id)
        if not regions:
            raise HTTPException(status_code=404, detail="No regions found")
        return {"regions": regions}
    finally:
        session.close()

@app.get("/simulations/{simulation_id}/farmers")
async def get_simulation_farmers(simulation_id: int):
    """Get farmers for a simulation"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        farmers = repository.get_simulation_farmers(simulation_id)
        if not farmers:
            raise HTTPException(status_code=404, detail="No farmers found")
        return {"farmers": farmers}
    finally:
        session.close()

@app.get("/simulations/{simulation_id}/policies")
async def get_simulation_policies(simulation_id: int):
    """Get policies for a simulation"""
    session = get_session()
    repository = SimulationRepository(session)
    try:
        policies = repository.get_simulation_policies(simulation_id)
        if not policies:
            raise HTTPException(status_code=404, detail="No policies found")
        return {"policies": policies}
    finally:
        session.close()

@app.get("/regions")
async def get_regions():
    """Get available regions"""
    return {
        "districts": DISTRICTS,
        "agro_ecological_zones": AGRO_ECOLOGICAL_ZONES
    }

@app.get("/crops")
async def get_crops():
    """Get available crops and their base yields"""
    return {
        "crops": CROPS,
        "base_yields": CROP_BASE_YIELDS
    }

@app.get("/policies")
async def get_policies():
    """Get available policy types"""
    return {
        "policy_types": POLICY_TYPES
    }

def generate_visualizations(results: dict, output_dir: Path, visualizer: SimulationVisualizer):
    """Generate all visualizations for the simulation results"""
    # Climate impact visualization
    climate_data = {region: {date: data['climate_impact'] 
                           for date, data in results.items()}
                   for region in DISTRICTS}
    visualizer.plot_climate_impact(climate_data, 
                                 save_path=output_dir / "climate_impact.png")
    
    # Production trends visualization
    production_data = {region: {date: {'production': data['production'],
                                     'market_price': data['market_price']}
                              for date, data in results.items()}
                      for region in DISTRICTS}
    visualizer.plot_production_trends(production_data,
                                    save_path=output_dir / "production_trends.png")
    
    # Risk map
    locations = {region: {'latitude': results[SIMULATION_START_DATE][region]['latitude'],
                         'longitude': results[SIMULATION_START_DATE][region]['longitude'],
                         'drought_risk': results[SIMULATION_END_DATE][region]['climate_impact']['drought_risk'],
                         'flood_risk': results[SIMULATION_END_DATE][region]['climate_impact']['flood_risk']}
                for region in DISTRICTS}
    visualizer.create_risk_map(locations,
                              save_path=output_dir / "risk_map.html")
    
    # Create comprehensive dashboard
    dashboard_data = {
        'climate_data': climate_data,
        'production_data': production_data,
        'market_data': {region: {date: data['market_price']
                               for date, data in results.items()}
                       for region in DISTRICTS},
        'risk_data': locations
    }
    visualizer.create_dashboard(dashboard_data,
                              save_path=output_dir / "dashboard.png") 