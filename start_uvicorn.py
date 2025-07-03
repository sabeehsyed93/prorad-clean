#!/usr/bin/env python3
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("start_uvicorn")

def main():
    """
    Start the FastAPI application using uvicorn.
    Uses PORT environment variable if available, otherwise defaults to 8000.
    """
    try:
        # Get port from environment variable or use default
        port = os.environ.get("PORT", "8000")
        # Ensure port is an integer
        try:
            port_int = int(port)
            port = str(port_int)  # Convert back to string for command
        except ValueError:
            logger.warning(f"Invalid PORT value: {port}, using default 8000")
            port = "8000"
            
        logger.info(f"Starting uvicorn on port {port}")
        
        # Start uvicorn with the FastAPI app
        cmd = [
            "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0",
            "--port", port
        ]
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Execute uvicorn with the specified parameters
        subprocess.run(cmd, check=True)
        
    except Exception as e:
        logger.error(f"Error starting uvicorn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
