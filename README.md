# Radiology Transcription Assistant

A web application to assist with radiology report transcription. This app listens to the microphone, transcribes speech in real-time, and processes the transcription using Claude AI to create structured, professional radiology reports.

## Features

- Real-time speech-to-text transcription using Whisper API
- LLM processing with Anthropic's Claude API to format and structure reports
- Template-based report generation
- Prompt management for customizing AI instructions
- Modern, responsive UI built with React and Material UI
- WebSocket connection for real-time updates

## Prompt Management Feature

The application includes a prompt management system that allows users to create, edit, delete, and activate different prompts for the AI model. This feature enables customization of how the AI processes and formats radiology reports.

### Key Features

- **Multiple Prompts**: Create and manage multiple prompts for different reporting styles or requirements
- **Default Prompt**: A non-deletable default prompt is always available
- **Active Prompt Selection**: Set any prompt as the active one to be used for report generation
- **Prompt Protection**: Default prompt cannot be deleted or modified to ensure system stability
- **Integration with Templates**: Prompts work alongside templates for comprehensive report customization

## Project Structure

```
ProRad_Clean/
├── main.py                # FastAPI backend application
├── database.py           # Database models and connection
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── frontend/             # React frontend
│   ├── src/              # Source code
│   │   ├── components/   # React components
│   │   │   ├── PromptManager.js  # Prompt management component
│   │   │   ├── TemplateManager.js # Template management component
│   │   │   └── ...       # Other components
│   │   ├── utils/        # Utility functions
│   │   ├── App.js        # Main application component
│   │   └── ...           # Other React files
│   └── package.json      # Node.js dependencies
└── DEPLOYMENT.md         # Deployment instructions
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file and add your API keys:
   ```
   CLAUDE_API_KEY=your_anthropic_api_key_here
   DATABASE_URL=your_database_url_here  # Optional, defaults to SQLite if not provided
   ```

4. Run the backend server:
   ```
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Create a `.env` file in the frontend directory (optional for development):
   ```
   REACT_APP_API_URL=http://localhost:8001
   ```

4. Start the development server:
   ```
   npm start
   ```

5. Open your browser and navigate to `http://localhost:3000`

## API Keys Required

- **Claude API Key**: Get from [Anthropic](https://www.anthropic.com/) for Claude AI access
- **Replicate API Token**: Get from [Replicate](https://replicate.com/) for Whisper API access

## Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## Usage

1. Open the application in your browser (typically at http://localhost:3000)
2. Click "Start Recording" to begin capturing audio
3. Speak clearly into your microphone
4. Click "Stop Recording" when finished
5. Select a template if desired
6. Click "Process with Gemini" to format the transcription
7. Copy or save the processed report

## Deployment

The application can be deployed to any hosting service that supports Node.js and Python applications. Consider services like Vercel, Netlify, or Railway for easy deployment.

## License

MIT
