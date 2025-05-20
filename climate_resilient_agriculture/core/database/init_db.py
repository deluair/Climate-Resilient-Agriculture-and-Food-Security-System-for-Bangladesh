import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from .session import get_db_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    """Initialize the database schema"""
    try:
        # Create database engine
        engine = create_engine(get_db_url())
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        logger.info("Database schema initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing database schema: {str(e)}")
        return False

def drop_db():
    """Drop all database tables"""
    try:
        # Create database engine
        engine = create_engine(get_db_url())
        
        # Drop all tables
        Base.metadata.drop_all(engine)
        
        logger.info("Database tables dropped successfully")
        return True
    except Exception as e:
        logger.error(f"Error dropping database tables: {str(e)}")
        return False

if __name__ == "__main__":
    # Initialize database when script is run directly
    init_db() 