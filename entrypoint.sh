#!/bin/bash

# Print environment information
echo "Environment information:"
echo "PORT: $PORT"
echo "DATABASE_URL: ${DATABASE_URL:0:20}..."
echo "RAILWAY_SERVICE_NAME: $RAILWAY_SERVICE_NAME"

# Run database initialization
echo "Running database initialization..."
python init_railway_db.py

# Set default port if not provided
if [ -z "$PORT" ]; then
    echo "PORT environment variable not set, using default port 8000"
    export PORT=8000
fi

# Start the application with explicit port from environment
echo "Starting application on port $PORT..."
python -m uvicorn main:app --host 0.0.0.0 --port "$PORT" --log-level debug
