from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL")

# Check for Railway PostgreSQL environment variables
PG_HOST = os.getenv("PGHOST")
PG_USER = os.getenv("PGUSER")
PG_PASSWORD = os.getenv("PGPASSWORD")
PG_DATABASE = os.getenv("POSTGRES_DB")
PG_PORT = os.getenv("PGPORT")

# If Railway PostgreSQL variables are present but no DATABASE_URL, construct it
if not DATABASE_URL and PG_HOST and PG_USER and PG_PASSWORD and PG_DATABASE:
    DATABASE_URL = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}"
    logger.info("Constructed PostgreSQL DATABASE_URL from Railway environment variables")

# Fallback to SQLite if no database connection info is available
if not DATABASE_URL:
    logger.warning("No DATABASE_URL found in environment, falling back to SQLite")
    DATABASE_URL = "sqlite:///./radiology_reports.db"

logger.info(f"Initializing database connection to: {DATABASE_URL.split('@')[0].split(':')[0]}")

# Handle PostgreSQL database URLs
if DATABASE_URL:
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    if "postgresql" in DATABASE_URL:
        logger.info("Using PostgreSQL database")
    else:
        logger.info("Using SQLite database")
else:
    logger.info("Using SQLite database")

# Configure SQLAlchemy engine with connection pooling and retry settings
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=1800,  # Recycle connections after 30 minutes
    echo=False  # Disable duplicate SQL logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

# Define models
class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    raw_transcription = Column(Text)
    processed_text = Column(Text)
    template_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    content = Column(Text)
    is_default = Column(Integer, default=0)  # 0 = not default, 1 = default
    is_active = Column(Integer, default=0)   # 0 = not active, 1 = active
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Successfully created database tables")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
