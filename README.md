# Climate-Resilient Agriculture and Food Security System for Bangladesh

A comprehensive simulation system for analyzing and predicting the impacts of climate change on agriculture and food security in Bangladesh.

## Features

- Multiple simulation scenarios (baseline, climate change, technology adoption)
- Market price forecasting and analysis
- Climate impact assessment
- Production trend analysis
- Risk mapping and visualization
- RESTful API for programmatic access
- Command-line interface for easy interaction
- Database storage for simulation results and configurations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/climate-resilient-agriculture.git
cd climate-resilient-agriculture
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
   - Create a `.env` file in the project root with the following variables:
     ```
     DATABASE_URL=postgresql://username:password@localhost:5432/climate_agriculture
     ```
   - Initialize the database:
     ```bash
     python -m climate_resilient_agriculture.scripts.run_migrations
     ```

## Usage

### Command-line Interface

1. Run a specific scenario:
```bash
python -m climate_resilient_agriculture.cli run-simulation --scenario baseline --start-date 2024-01-01 --end-date 2024-12-31
```

2. Run all scenarios and compare results:
```bash
python -m climate_resilient_agriculture.cli run-all-scenarios
```

3. Start the API server:
```bash
python -m climate_resilient_agriculture.cli start-api
```

### API

1. Start the API server:
```bash
python -m climate_resilient_agriculture.scripts.run_api
```

2. Access the API documentation at `http://localhost:8000/docs`

3. Example API requests:
```bash
# Get available scenarios
curl http://localhost:8000/scenarios

# Run a simulation
curl -X POST http://localhost:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2024-01-01T00:00:00",
    "end_date": "2024-12-31T23:59:59",
    "scenario_type": "baseline",
    "parameters": {
      "farmer_count": 100,
      "infrastructure_per_district": 5
    }
  }'

# Get simulation results
curl http://localhost:8000/simulations/1
```

## Project Structure

```
climate_resilient_agriculture/
├── api/
│   └── main.py                 # FastAPI application
├── core/
│   ├── database/
│   │   ├── models.py          # SQLAlchemy models
│   │   ├── repository.py      # Database operations
│   │   ├── session.py         # Database session management
│   │   └── migrations/        # Database migrations
│   ├── simulation_engine.py   # Simulation logic
│   ├── data_generator.py      # Data generation utilities
│   └── visualization.py       # Visualization module
├── config/
│   └── simulation_config.py   # Simulation parameters
├── scripts/
│   ├── run_api.py            # API server script
│   ├── run_scenarios.py      # Scenario execution script
│   └── run_migrations.py     # Database migration script
├── tests/
│   ├── test_simulation.py    # Simulation tests
│   └── test_api.py          # API tests
├── cli.py                    # Command-line interface
├── requirements.txt          # Project dependencies
└── README.md                # Project documentation
```

## Configuration

The simulation parameters can be adjusted in `climate_resilient_agriculture/config/simulation_config.py`:

- Time parameters (start date, end date, time step)
- Region parameters (districts, agro-ecological zones)
- Crop parameters (types, base yields)
- Climate parameters (base temperature, rainfall, changes)
- Farmer parameters (count, land holding sizes)
- Infrastructure parameters (types, capacities)
- Policy parameters (count, budget ranges)
- Market parameters (base prices, growth rates)
- Technology adoption parameters (rates, levels)
- Risk parameters (thresholds for drought, flood, salinity)
- Output parameters (directory, visualization formats)

## Database Schema

The system uses PostgreSQL to store simulation data with the following tables:

- `simulations`: Stores simulation metadata and results
- `regions`: Contains region-specific data
- `farmers`: Stores farmer profiles and attributes
- `policies`: Contains policy information
- `climate_data`: Stores climate measurements
- `production_data`: Contains production and market data

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Bangladesh Agricultural Research Institute (BARI)
- Bangladesh Rice Research Institute (BRRI)
- International Rice Research Institute (IRRI)
- Food and Agriculture Organization (FAO)
- World Bank

## Contact

For questions and support, please contact:
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername) 