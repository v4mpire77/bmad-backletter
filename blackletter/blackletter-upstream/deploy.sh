#!/bin/bash
# Blackletter Systems Deployment Script for Render.com

# Check if render-cli is installed
if ! command -v render &> /dev/null; then
    echo "Render CLI not found. Installing..."
    npm install -g @render/cli
fi

# Check if logged in to Render
if ! render whoami 2>&1 | grep -q "Logged in as"; then
    echo "Please log in to Render:"
    render login
fi

# Deploy using Blueprint
echo "Deploying to Render.com..."
render blueprint launch

echo "Deployment initiated!"
echo "Check your Render dashboard for deployment status: https://dashboard.render.com"
echo "Once deployed, your application will be available at: https://blackletter.onrender.com"
