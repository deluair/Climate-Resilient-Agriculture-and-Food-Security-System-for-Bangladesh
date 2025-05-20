from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variable or use SQLite as default
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///climate_agriculture.db')

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800
)

# Create session factory
session_factory = sessionmaker(bind=engine)

# Create thread-safe session
Session = scoped_session(session_factory)

def get_session():
    """Get a database session"""
    session = Session()
    try:
        yield session
    finally:
        session.close()

def init_db():
    """Initialize the database"""
    from .models import Base
    Base.metadata.create_all(engine)

def close_db():
    """Close database connections"""
    Session.remove()
    engine.dispose() 