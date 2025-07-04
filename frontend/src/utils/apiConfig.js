// Get the API URL from environment variables, fallback to localhost for development
// For production deployment on Railway/Netlify, set REACT_APP_API_URL in the Netlify environment variables
// Example: https://your-railway-app-name.up.railway.app
export const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8001';

// API endpoint paths
const API_ENDPOINTS = {
    'templates': 'templates',
    'process': 'process',
    'prompts': 'prompts',
    'prompts/active': 'prompts/active',
    'recent-reports': 'recent-reports',
    'health': 'health'
};

// Helper function to build API endpoints
export const getApiEndpoint = (path) => {
    // Check if path is a known endpoint
    if (API_ENDPOINTS[path]) {
        return `${API_URL}/${API_ENDPOINTS[path]}`;
    }
    
    // For dynamic paths like 'prompts/1' or 'templates/chest_xray'
    // Remove leading slash if present
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `${API_URL}/${cleanPath}`;
};
