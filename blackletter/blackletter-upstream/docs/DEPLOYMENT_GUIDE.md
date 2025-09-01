# Deployment Guide for Blackletter Systems

This guide explains how to deploy Blackletter Systems to Render.com.

## Prerequisites

1. A [Render.com](https://render.com) account
2. An S3-compatible storage service (AWS S3, DigitalOcean Spaces, etc.)
3. OpenAI API key (or other LLM provider API key)

## Deployment Steps

### 1. Fork or Clone the Repository

Make sure you have the latest version of the code in your own repository.

### 2. Prepare Deployment Scripts

If you're on Linux/macOS, make the deployment scripts executable:

```bash
chmod +x deploy.sh start.sh
```

On Windows, you can run the PowerShell scripts directly.

### 3. Connect to Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click on the "New +" button and select "Blueprint"
3. Connect your GitHub/GitLab account and select your repository
4. Select the repository containing the Blackletter Systems code

### 4. Configure the Blueprint

Render will automatically detect the `render.yaml` file in your repository and create the necessary services:

- `blackletter-frontend`: Next.js frontend application
- `blackletter-api`: FastAPI backend application
- `blackletter-db`: PostgreSQL database

### 5. Set Environment Variables

You'll need to set the following environment variables for the `blackletter-api` service:

- `S3_ACCESS_KEY`: Your S3 access key
- `S3_SECRET_KEY`: Your S3 secret key
- `S3_BUCKET`: Your S3 bucket name (default: `blackletter-prod`)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)

### 6. Create S3 Bucket

Make sure to create an S3 bucket with the name specified in your environment variables.

### 7. Deploy

Click "Apply" to start the deployment process. Render will:

1. Create a PostgreSQL database
2. Build and deploy the backend API
3. Build and deploy the frontend application

### 8. Access Your Application

Once deployment is complete, you can access your application at:

- Frontend: `https://blackletter.onrender.com`
- API: `https://blackletter-api.onrender.com`
- API Documentation: `https://blackletter-api.onrender.com/docs`

## Alternative Free Hosting Options

If Render doesn't meet your needs, here are some alternative free hosting options:

### Railway

[Railway](https://railway.app/) offers a generous free tier and easy deployment:

1. Create a `railway.json` file in your repository
2. Connect your GitHub repository to Railway
3. Configure environment variables
4. Deploy

### Vercel + Heroku

You can also use a combination of:

- [Vercel](https://vercel.com/) for the Next.js frontend (generous free tier)
- [Heroku](https://heroku.com/) for the FastAPI backend (free tier with limitations)

### Fly.io

[Fly.io](https://fly.io/) offers a free tier that includes:

- 3 shared-cpu-1x 256mb VMs
- 3GB persistent volume storage
- 160GB outbound data transfer

Create a `fly.toml` file to configure your deployment.

## Monitoring and Scaling

Once your application is deployed, you can:

1. Monitor performance in the Render dashboard
2. Set up alerts for errors or high resource usage
3. Upgrade to paid plans for better performance and more resources when needed

## Troubleshooting

If you encounter issues during deployment:

1. Check the build logs in the Render dashboard
2. Verify that all environment variables are set correctly
3. Ensure your S3 bucket exists and is accessible
4. Check that your database connection string is valid
