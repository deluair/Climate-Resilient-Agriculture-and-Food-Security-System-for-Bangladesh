from datetime import datetime, timedelta
from typing import Dict, List

# Simulation time parameters
SIMULATION_START_DATE = datetime(2024, 1, 1)
SIMULATION_END_DATE = datetime(2024, 12, 31)
SIMULATION_TIME_STEP = timedelta(days=1)

# Region parameters
DISTRICTS = [
    "Dhaka", "Chittagong", "Khulna", "Rajshahi", "Barishal",
    "Sylhet", "Rangpur", "Mymensingh", "Comilla", "Noakhali"
]

AGRO_ECOLOGICAL_ZONES = [
    "Coastal Zone", "Haor Basin", "Barind Tract",
    "Chittagong Hill Tracts", "Floodplains", "Char Islands"
]

# Crop parameters
CROPS = [
    "Rice", "Wheat", "Maize", "Potato", "Jute",
    "Sugarcane", "Vegetables", "Fruits"
]

CROP_BASE_YIELDS = {
    "Rice": 4.0,  # tons per hectare
    "Wheat": 3.0,
    "Maize": 5.0,
    "Potato": 20.0,
    "Jute": 2.5,
    "Sugarcane": 60.0,
    "Vegetables": 15.0,
    "Fruits": 10.0
}

# Climate parameters
BASE_TEMPERATURE = 25.0  # Celsius
BASE_RAINFALL = 2000.0  # mm per year
TEMPERATURE_CHANGE_MEAN = 0.5  # Celsius per year
TEMPERATURE_CHANGE_STD = 0.2
RAINFALL_CHANGE_MEAN = -100  # mm per year
RAINFALL_CHANGE_STD = 50

# Farmer parameters
FARMER_COUNT = 1000
MIN_LAND_HOLDING = 0.1  # hectares
MAX_LAND_HOLDING = 10.0  # hectares
MIN_FARMING_EXPERIENCE = 1  # years
MAX_FARMING_EXPERIENCE = 40  # years

# Infrastructure parameters
INFRASTRUCTURE_TYPES = ["storage", "irrigation", "transportation"]
INFRASTRUCTURE_PER_DISTRICT = 5
MIN_INFRASTRUCTURE_CAPACITY = 100  # tons or cubic meters
MAX_INFRASTRUCTURE_CAPACITY = 10000  # tons or cubic meters

# Policy parameters
POLICY_COUNT = 10
POLICY_TYPES = [
    "subsidy", "credit", "insurance", "technology_adoption",
    "infrastructure_development", "research_development"
]
MIN_POLICY_BUDGET = 1000000  # BDT
MAX_POLICY_BUDGET = 1000000000  # BDT

# Market parameters
BASE_PRICE = 1000  # BDT per ton
PRICE_VOLATILITY = 0.2  # Standard deviation of price changes
DEMAND_GROWTH_RATE = 0.05  # 5% annual growth

# Technology adoption parameters
TECHNOLOGY_ADOPTION_RATE = 0.1  # 10% annual increase
MAX_TECHNOLOGY_LEVEL = 1.0
MIN_TECHNOLOGY_LEVEL = 0.0

# Risk parameters
DROUGHT_RISK_THRESHOLD = 0.7
FLOOD_RISK_THRESHOLD = 0.7
SALINITY_RISK_THRESHOLD = 0.6

# Output parameters
OUTPUT_DIRECTORY = "output"
VISUALIZATION_FORMATS = ["png", "html", "json"] 