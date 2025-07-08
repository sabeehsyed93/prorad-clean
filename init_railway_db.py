#!/usr/bin/env python3
"""
Database initialization script for Railway deployment.
This script will:
1. Connect to the Railway PostgreSQL database
2. Create all necessary tables if they don't exist
3. Initialize default templates and prompts
4. Verify the database connection and table structure
"""

import os
import sys
import logging
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import database models and functions
try:
    from database import (
        engine, SessionLocal, Base, create_tables,
        Template as DBTemplate, Prompt as DBPrompt, Report
    )
except ImportError as e:
    logger.error(f"Failed to import database modules: {e}")
    sys.exit(1)

# Import default templates and prompts from main
try:
    from main import default_templates, default_system_prompt
except ImportError as e:
    logger.error(f"Failed to import defaults from main: {e}")
    default_system_prompt = """You are an expert radiologist with years of experience in dictating and writing radiology reports. Your task is to convert the transcribed dictation into a properly formatted and professional radiology report.

Follow these guidelines:
1. Maintain medical accuracy and terminology
2. Organize content into appropriate sections
3. Correct any speech recognition errors that are obvious
4. Format the report professionally
5. If a template is provided, use it to structure the report
6. Preserve all medical findings and observations from the original dictation

Do not:
1. Add medical findings not mentioned in the dictation
2. Remove important medical details from the dictation
3. Change the meaning of any medical observations
4. Use overly complex formatting

The output should be a clean, professional radiology report that accurately reflects the dictated content."""
    
    default_templates = {
        "chest_xray": """
# Chest X-ray Report Template

## Clinical Information
[clinical_information]

## Technique
[technique]

## Findings
[findings]

## Impression
[impression]
""",
        "abdominal_ct": """
# Abdominal CT Report Template

## Clinical Information
[clinical_information]

## Technique
[technique]

## Findings
### Liver
[liver_findings]

### Gallbladder and Biliary System
[biliary_findings]

### Pancreas
[pancreas_findings]

### Spleen
[spleen_findings]

### Adrenal Glands
[adrenal_findings]

### Kidneys and Ureters
[kidney_findings]

### GI Tract
[gi_findings]

### Vascular
[vascular_findings]

### Other Findings
[other_findings]

## Impression
[impression]
"""
    }

def check_database_connection():
    """Check if we can connect to the database"""
    try:
        connection = engine.connect()
        connection.close()
        logger.info("✅ Successfully connected to the database")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to connect to the database: {e}")
        return False

def check_tables_exist():
    """Check if all required tables exist"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    required_tables = ['templates', 'prompts', 'reports']
    
    logger.info(f"Found tables: {tables}")
    
    missing_tables = [table for table in required_tables if table not in tables]
    if missing_tables:
        logger.warning(f"❌ Missing tables: {missing_tables}")
        return False
    else:
        logger.info("✅ All required tables exist")
        return True

def create_all_tables():
    """Create all tables defined in Base"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Successfully created all tables")
        return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to create tables: {e}")
        return False

def initialize_default_data():
    """Initialize default templates and prompts"""
    try:
        with SessionLocal() as db:
            # Initialize templates
            for name, content in default_templates.items():
                existing = db.query(DBTemplate).filter(DBTemplate.name == name).first()
                if not existing:
                    template = DBTemplate(name=name, content=content)
                    db.add(template)
                    logger.info(f"Added template: {name}")
                else:
                    logger.info(f"Template already exists: {name}")
            
            # Initialize default prompt
            default_prompt = db.query(DBPrompt).filter(DBPrompt.is_default == 1).first()
            if not default_prompt:
                default_prompt = DBPrompt(
                    name="Default Radiologist Prompt",
                    content=default_system_prompt,
                    is_default=1,
                    is_active=1
                )
                db.add(default_prompt)
                logger.info("Added default prompt")
            else:
                logger.info("Default prompt already exists")
            
            db.commit()
            logger.info("✅ Successfully initialized default data")
            return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to initialize default data: {e}")
        return False

def verify_database_setup():
    """Verify database setup by querying each table"""
    try:
        with SessionLocal() as db:
            template_count = db.query(DBTemplate).count()
            prompt_count = db.query(DBPrompt).count()
            report_count = db.query(Report).count()
            
            logger.info(f"Templates: {template_count}")
            logger.info(f"Prompts: {prompt_count}")
            logger.info(f"Reports: {report_count}")
            
            # Check if default prompt is active
            active_prompt = db.query(DBPrompt).filter(DBPrompt.is_active == 1).first()
            if active_prompt:
                logger.info(f"Active prompt: {active_prompt.name}")
            else:
                logger.warning("❌ No active prompt found")
                
            return True
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to verify database setup: {e}")
        return False

def run_raw_sql(sql):
    """Run raw SQL for debugging purposes"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text(sql))
            return result
    except SQLAlchemyError as e:
        logger.error(f"❌ Failed to execute SQL: {e}")
        return None

def main():
    """Main function to initialize and verify database"""
    logger.info("Starting database initialization script")
    
    # Check database connection
    if not check_database_connection():
        logger.error("Database connection failed. Exiting.")
        sys.exit(1)
    
    # Check if tables exist
    tables_exist = check_tables_exist()
    
    # Create tables if they don't exist
    if not tables_exist:
        logger.info("Creating tables...")
        if not create_all_tables():
            logger.error("Failed to create tables. Exiting.")
            sys.exit(1)
    
    # Initialize default data
    if not initialize_default_data():
        logger.error("Failed to initialize default data. Exiting.")
        sys.exit(1)
    
    # Verify database setup
    if not verify_database_setup():
        logger.error("Failed to verify database setup. Exiting.")
        sys.exit(1)
    
    logger.info("✅ Database initialization completed successfully")

if __name__ == "__main__":
    main()
