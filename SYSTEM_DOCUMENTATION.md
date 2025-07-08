# ProRad System Documentation

## System Overview

ProRad is a radiology transcription assistant that helps radiologists convert their spoken dictations into professionally formatted reports. The system consists of two main components:

1. **Backend (FastAPI)**: Handles API requests, database operations, and integration with Claude AI for report processing
2. **Frontend (React)**: Provides a user interface for transcription, report management, template management, and prompt management

### Key Features

- Speech-to-text transcription using Whisper API
- AI-powered report formatting using Claude API
- Template management for structured reports
- Prompt management for customizing AI behavior
- Report history and retrieval
- Real-time processing

## Architecture

### Backend Components

- **FastAPI Framework**: Provides the REST API endpoints
- **SQLAlchemy ORM**: Database interaction layer
- **Claude API Integration**: For AI-powered report processing
- **PostgreSQL Database**: Stores templates, prompts, and reports

### Frontend Components

- **React**: UI framework
- **Material UI**: Component library
- **React Hooks**: State management
- **Fetch API**: Backend communication

### Database Schema

- **Templates**: Stores report templates
- **Prompts**: Stores AI instruction prompts
- **Reports**: Stores processed reports

## Deployment Issues and Solutions

### Issue 1: Port Configuration

**Problem**: Railway deployment failed with error: "Invalid value for '--port': '$PORT' is not a valid integer"

**Solution**: 
- Removed explicit port specification in railway.toml and Procfile
- Updated to use `python -m uvicorn main:app --host 0.0.0.0` without specifying port
- Railway automatically assigns the port at runtime

### Issue 2: PostgreSQL Connection

**Problem**: Application couldn't connect to Railway PostgreSQL database

**Solution**:
- Enhanced database.py to detect Railway PostgreSQL environment variables
- Added logic to construct PostgreSQL connection string from individual variables
- Improved error handling and logging for database connections

### Issue 3: Health Check Endpoint

**Problem**: Railway health check failing

**Solution**:
- Ensured both `/health` and `/_health` endpoints are properly implemented
- Updated railway.toml to use the correct healthcheck path
- Added HEAD request support for health endpoints

### Issue 4: Model Import Confusion

**Problem**: Confusion between SQLAlchemy model and Pydantic model both named `Prompt`

**Solution**:
- Renamed SQLAlchemy model import to `DBPrompt` to avoid naming conflicts
- Updated all database queries to use the correct model name

### Issue 5: API URL Configuration

**Problem**: Frontend configured to use incorrect backend port

**Solution**:
- Updated API URL in apiConfig.js to use the correct port
- Added environment variable support for deployment

## Prompt Management Feature

The prompt management feature allows users to create, edit, delete, and activate different prompts for the AI model. This enables customization of how Claude processes and formats radiology reports.

### How Prompts Work with Claude

1. **System Prompt**: The active prompt is used as the system prompt for Claude, setting the overall tone and approach
2. **Template Integration**: If a template is selected, it's appended to the system prompt with instructions
3. **User Prompt**: Contains the transcribed speech to be processed

Example flow:
```
System Prompt: "You are an expert radiologist writing a radiology report..."
+ Template (if selected): "Use the following template structure: [template content]"
User Prompt: "Here is the transcribed speech to convert into a professional report: [transcription]"
```

### Database Structure

The `prompts` table includes:
- id: Primary key
- name: Prompt name
- content: The actual prompt text
- is_default: Flag for the default prompt (0 or 1)
- is_active: Flag for the currently active prompt (0 or 1)
- created_at/updated_at: Timestamps

### API Endpoints

- GET /prompts - List all prompts
- GET /prompts/active - Get the currently active prompt
- POST /prompts - Create a new prompt
- PUT /prompts/{id} - Update a prompt
- POST /prompts/{id}/activate - Activate a prompt
- DELETE /prompts/{id} - Delete a prompt

## Deployment Instructions

### Railway Deployment

1. **Environment Variables**:
   - CLAUDE_API_KEY: Your Anthropic API key
   - PostgreSQL variables are automatically set by Railway

2. **Database**:
   - PostgreSQL database is provisioned by Railway
   - Tables are created automatically on first run

3. **Deployment Configuration**:
   - railway.toml contains deployment settings
   - Procfile specifies the command to start the application

### Netlify Deployment

1. **Environment Variables**:
   - REACT_APP_API_URL: URL of your Railway backend

2. **Build Settings**:
   - Build command: `cd frontend && npm install && npm run build`
   - Publish directory: `frontend/build`

## Troubleshooting Guide

### Backend Issues

1. **Database Connection Errors**:
   - Check PostgreSQL environment variables
   - Verify database URL format
   - Check database logs in Railway

2. **API Errors**:
   - Check application logs in Railway
   - Verify API key is set correctly
   - Test endpoints with curl or Postman

3. **Deployment Failures**:
   - Check railway.toml configuration
   - Verify Procfile format
   - Check for syntax errors in Python code

### Frontend Issues

1. **API Connection Errors**:
   - Verify REACT_APP_API_URL is set correctly
   - Check for CORS issues
   - Test API endpoints directly

2. **UI Rendering Issues**:
   - Check browser console for errors
   - Verify React component props
   - Test with different browsers

## Future Improvements

1. **Authentication**: Add user authentication and authorization
2. **Advanced Prompt Features**: Add categories, tags, and search for prompts
3. **Report Analytics**: Add analytics for report generation and usage
4. **Enhanced UI**: Improve user experience with better feedback and animations
5. **Mobile Support**: Optimize UI for mobile devices
