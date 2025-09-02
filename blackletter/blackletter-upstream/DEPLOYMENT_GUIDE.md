# Blackletter Systems - Render Deployment Guide

## Overview
This guide will help you deploy the Blackletter Systems application on Render, including both the backend API and frontend.

## Prerequisites
- A Render account
- Your application code pushed to a Git repository (GitHub, GitLab, etc.)

## Deployment Steps

### 1. Connect Your Repository
1. Log in to [Render Dashboard](https://dashboard.render.com)
2. Click "New +" and select "Blueprint"
3. Connect your Git repository
4. Render will automatically detect the `render.yaml` file

### 2. Environment Variables Setup
Before deploying, you'll need to set up the following environment variables in Render:

#### Backend Environment Variables
- `OPENAI_API_KEY` - Your OpenAI API key
- `GOOGLE_API_KEY` - Your Google API key (if using Gemini)
- `PORT` - Will be set automatically by Render

#### Frontend Environment Variables
- `NEXT_PUBLIC_API_URL` - Will be set to `https://blackletter-backend.onrender.com`
- `PORT` - Will be set automatically by Render

### 3. Deploy Using Blueprint
1. Render will automatically create two services:
   - **blackletter-backend**: Python FastAPI service
   - **blackletter-frontend**: Next.js frontend service

2. The deployment will use the configuration from `render.yaml`

### 4. Manual Service Creation (Alternative)
If you prefer to create services manually:

#### Backend Service
- **Type**: Web Service
- **Runtime**: Python 3.11
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Root Directory**: `backend`

#### Frontend Service
- **Type**: Web Service
- **Runtime**: Node.js 18.17.0
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npm start`
- **Root Directory**: `frontend`

### 5. Post-Deployment Configuration

#### Update Frontend API URL
After the backend is deployed, update the frontend environment variable:
- Go to your frontend service settings
- Update `NEXT_PUBLIC_API_URL` to your actual backend URL
- Redeploy the frontend service

#### Verify CORS Settings
The backend is configured to allow requests from:
- `http://localhost:3000` (local development)
- `https://blackletter-frontend.onrender.com`
- `https://blackletter-systems.onrender.com`

## Service URLs
After deployment, your services will be available at:
- **Backend API**: `https://blackletter-backend.onrender.com`
- **Frontend**: `https://blackletter-frontend.onrender.com`

## Health Check
You can verify the backend is working by visiting:
`https://blackletter-backend.onrender.com/health`

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check the build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **CORS Errors**
   - Verify the frontend URL is in the backend CORS allowlist
   - Check that `NEXT_PUBLIC_API_URL` is set correctly

3. **Environment Variables**
   - Ensure all required API keys are set in Render
   - Check that variable names match exactly

4. **Port Issues**
   - Render automatically sets the `PORT` environment variable
   - The application should use `$PORT` in the start command

### Logs and Monitoring
- View logs in the Render dashboard for each service
- Monitor service health and performance
- Set up alerts for service downtime

## Security Considerations
- Never commit API keys to your repository
- Use Render's environment variable system for sensitive data
- Enable HTTPS (automatic on Render)
- Consider setting up custom domains

## Cost Optimization
- Render offers a free tier for development
- Monitor usage to avoid unexpected charges
- Consider auto-sleep for development environments

## Support
For Render-specific issues, refer to:
- [Render Documentation](https://render.com/docs)
- [Render Support](https://render.com/support)
