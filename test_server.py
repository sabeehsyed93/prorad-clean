#!/usr/bin/env python3
from fastapi import FastAPI
import uvicorn

# Create a minimal FastAPI app
app = FastAPI()

@app.get("/_health")
async def health_check():
    """Health check endpoint for Railway deployment"""
    return {"status": "ok"}

@app.get("/")
async def root():
    return {"message": "Test server is running"}

if __name__ == "__main__":
    # Run the server with a hardcoded port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
