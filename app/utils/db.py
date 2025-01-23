from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from app.models import Base  # Import shared Base
from app.models.user import User  # Ensure models are registered
from app.models.task import Task  # Ensure models are registered

# Load environment variables
load_dotenv()

# Get the database URL from the .env file or fallback to SQLite for local testing
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session_local():
    """
    Yield a database session for dependency injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize the database by creating all tables defined in the models.
    """
    print(f"Initializing database with URL: {DATABASE_URL}")
    
    # Debug: Check which tables are being registered
    for table_name in Base.metadata.tables.keys():
        print(f"Registering table: {table_name}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("Database initialization complete.")
