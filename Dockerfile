FROM node:18-slim

WORKDIR /app

# Install Python and other dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    curl \
    procps \
    net-tools \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python3 -m venv /app/venv

# Copy and install Node.js dependencies
COPY package.json ./
RUN npm install

# Copy and install Python dependencies
COPY requirements.txt ./
RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt && \
    /app/venv/bin/pip install --no-cache-dir uvicorn fastapi

# Verify uvicorn and fastapi installation
RUN /app/venv/bin/uvicorn --version && \
    /app/venv/bin/pip list | grep uvicorn && \
    /app/venv/bin/pip list | grep fastapi

# Copy application code
COPY . .

# Ensure our Python startup scripts are executable
COPY start_uvicorn.py /app/start_uvicorn.py
RUN chmod +x /app/start_uvicorn.py

# Create start script
RUN echo '#!/bin/bash\n\
export PATH="/app/venv/bin:$PATH"\n\
exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}' > /app/start.sh && \
chmod +x /app/start.sh

# Set environment variables
ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:${PORT:-8000}/_health || exit 1

# Start command
CMD ["/app/start.sh"]
