#!/bin/bash
export PATH="/app/venv/bin:$PATH"

# Ensure PORT is set and is a valid integer
if [ -z "$PORT" ]; then
  PORT=8000
fi

# Validate PORT is an integer
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "Warning: PORT environment variable is not a valid integer: '$PORT'. Using default 8000."
  PORT=8000
fi

echo "Starting uvicorn on port $PORT"
exec uvicorn main:app --host 0.0.0.0 --port $PORT
