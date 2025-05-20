import os
import sys
from alembic.config import Config
from alembic import command

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

def run_migrations():
    """Run database migrations"""
    # Get the path to the alembic.ini file
    alembic_ini_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'core',
        'database',
        'migrations',
        'alembic.ini'
    )
    
    # Create Alembic configuration
    alembic_cfg = Config(alembic_ini_path)
    
    try:
        # Run the migration
        command.upgrade(alembic_cfg, "head")
        print("Database migrations completed successfully")
    except Exception as e:
        print(f"Error running migrations: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_migrations() 