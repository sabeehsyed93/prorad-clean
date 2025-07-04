#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn
import os
import logging
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("minimal_server")

# Create a minimal FastAPI app
app = FastAPI()

# Log environment variables at startup
def log_environment():
    logger.info("Environment variables:")
    # Log PORT
    port = os.environ.get("PORT")
    logger.info(f"PORT: {port}")
    
    # Log DATABASE_URL (safely)
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        # Parse and log database connection details safely
        try:
            # Split the URL to extract components
            if '@' in db_url:
                credentials, location = db_url.split('@', 1)
                protocol = credentials.split('://')[0] if '://' in credentials else 'unknown'
                host = location.split('/')[0] if '/' in location else location
                logger.info(f"DATABASE_URL: {protocol}://*****@{host}")
                logger.info(f"Database type: {protocol}")
                logger.info(f"Database host: {host}")
            else:
                # For SQLite or other formats without credentials
                logger.info(f"DATABASE_URL: {db_url.split('://')[0]}://<rest-hidden>")
        except Exception as e:
            logger.error(f"Error parsing DATABASE_URL: {str(e)}")
    else:
        logger.info("DATABASE_URL not set")
    
    # Log other relevant environment variables
    logger.info(f"RAILWAY_ENVIRONMENT: {os.environ.get('RAILWAY_ENVIRONMENT', 'Not set')}")
    logger.info(f"RAILWAY_SERVICE_NAME: {os.environ.get('RAILWAY_SERVICE_NAME', 'Not set')}")

# Call at startup
log_environment()

@app.get("/_health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {"status": "ok"}

@app.head("/_health")
async def health_check_head():
    """Health check endpoint for HEAD requests"""
    return {"status": "ok"}

@app.get("/")
async def root():
    """Root endpoint"""
    # Get all environment variables (safely)
    env_vars = {}
    for key, value in os.environ.items():
        # Hide sensitive values
        if key in ['DATABASE_URL', 'ANTHROPIC_API_KEY', 'GEMINI_API_KEY', 'API_KEY']:
            if value:
                env_vars[key] = f"{value[:3]}...{value[-3:]} (length: {len(value)})"
            else:
                env_vars[key] = "Not set"
        else:
            env_vars[key] = value
    
    # Parse DATABASE_URL if it exists
    db_info = {}
    db_url = os.environ.get("DATABASE_URL")
    if db_url:
        try:
            if '@' in db_url:
                credentials, location = db_url.split('@', 1)
                protocol = credentials.split('://')[0] if '://' in credentials else 'unknown'
                host = location.split('/')[0] if '/' in location else location
                db_name = location.split('/')[-1] if '/' in location else 'unknown'
                db_info = {
                    "type": protocol,
                    "host": host,
                    "database": db_name
                }
            else:
                db_info = {"type": "sqlite or other", "path": "hidden"}
        except Exception as e:
            db_info = {"error": str(e)}
    
    return {
        "message": "Minimal server is running",
        "port": os.environ.get("PORT", "Not set"),
        "database_info": db_info,
        "railway_environment": os.environ.get("RAILWAY_ENVIRONMENT", "Not set"),
        "railway_service": os.environ.get("RAILWAY_SERVICE_NAME", "Not set")
    }

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = os.environ.get("PORT", "8000")
    try:
        port_int = int(port)
    except ValueError:
        logger.warning(f"Invalid PORT value: {port}, using default 8000")
        port_int = 8000
        
    logger.info(f"Starting minimal server on port {port_int}")
    uvicorn.run(app, host="0.0.0.0", port=port_int)
