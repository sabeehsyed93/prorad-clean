# ProRad Deployment Guide

This guide provides instructions for deploying the ProRad application to Railway (backend) and Netlify (frontend).

## Backend Deployment (Railway)

### Prerequisites
- A Railway account (https://railway.app/)
- A PostgreSQL database (can be provisioned on Railway)
- Anthropic API key for Claude

### Steps

1. **Push your code to GitHub**
   - Create a new GitHub repository
   - Push your code to the repository

2. **Create a new project on Railway**
   - Log in to Railway
   - Click "New Project" > "Deploy from GitHub repo"
   - Select your GitHub repository

3. **Add a PostgreSQL database**
   - In your Railway project, click "New" > "Database" > "PostgreSQL"
   - This will provision a PostgreSQL database for your application

4. **Set environment variables**
   - In your Railway project settings, add the following environment variables:
     - `PORT`: 8000 (or any port you prefer)
     - `CLAUDE_API_KEY`: Your Anthropic API key
     - `DATABASE_URL`: This should be automatically set by Railway when you add the PostgreSQL database

5. **Deploy the application**
   - Railway will automatically deploy your application when you push changes to your GitHub repository
   - You can also manually trigger a deployment from the Railway dashboard

6. **Get your deployment URL**
   - Once deployed, Railway will provide a URL for your application (e.g., https://your-app-name.up.railway.app)
   - Save this URL for configuring the frontend

## Frontend Deployment (Netlify)

### Prerequisites
- A Netlify account (https://www.netlify.com/)
- Your backend deployed on Railway

### Steps

1. **Build the frontend**
   - In your local environment, navigate to the frontend directory
   - Run `npm run build` to create a production build

2. **Create a new site on Netlify**
   - Log in to Netlify
   - Click "New site from Git"
   - Select your GitHub repository
   - Set the build command to `cd frontend && npm install && npm run build`
   - Set the publish directory to `frontend/build`

3. **Set environment variables**
   - In your Netlify site settings, add the following environment variable:
     - `REACT_APP_API_URL`: The URL of your Railway backend (e.g., https://your-app-name.up.railway.app)

4. **Configure CORS on the backend**
   - Make sure your backend allows requests from your Netlify domain
   - The current CORS configuration in `main.py` should already allow all origins, but you may want to restrict it to just your Netlify domain for security

5. **Deploy the frontend**
   - Netlify will automatically deploy your frontend when you push changes to your GitHub repository
   - You can also manually trigger a deployment from the Netlify dashboard

6. **Access your application**
   - Once deployed, Netlify will provide a URL for your application (e.g., https://your-app-name.netlify.app)
   - You can also configure a custom domain in the Netlify settings

## Troubleshooting

### Backend Issues
- Check the Railway logs for any errors
- Verify that all environment variables are set correctly
- Make sure the PostgreSQL database is properly connected

### Frontend Issues
- Check the Netlify build logs for any errors
- Verify that the `REACT_APP_API_URL` is set correctly
- Check browser console for any CORS errors

### API Connection Issues
- Ensure that the backend is properly handling CORS
- Verify that the frontend is using the correct API URL
- Check network requests in the browser developer tools

## Updating the Application

### Backend Updates
1. Push changes to your GitHub repository
2. Railway will automatically deploy the changes

### Frontend Updates
1. Push changes to your GitHub repository
2. Netlify will automatically deploy the changes

## Monitoring and Maintenance

### Backend
- Use Railway's monitoring tools to track application performance
- Set up alerts for any critical issues

### Frontend
- Use Netlify's analytics to track user engagement
- Monitor for any client-side errors

## Security Considerations

- Keep your API keys secure and never commit them to your repository
- Use environment variables for all sensitive information
- Consider implementing authentication for your API endpoints
- Regularly update dependencies to patch security vulnerabilities
