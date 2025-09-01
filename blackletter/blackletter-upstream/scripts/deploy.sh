#!/bin/bash

# Blackletter Systems - Render Deployment Script
# This script helps prepare and deploy the application to Render

echo "🚀 Blackletter Systems - Render Deployment"
echo "=========================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/blackletter-systems.git"
    echo "   git push -u origin main"
    exit 1
fi

echo "✅ Git repository configured"

# Check if render.yaml exists
if [ ! -f "render.yaml" ]; then
    echo "❌ render.yaml not found. Please ensure the deployment configuration exists."
    exit 1
fi

echo "✅ render.yaml found"

# Check backend requirements
if [ ! -f "src/backend/requirements.txt" ]; then
    echo "❌ src/backend/requirements.txt not found"
    exit 1
fi

echo "✅ Backend requirements found"

# Check frontend package.json
if [ ! -f "frontend/package.json" ]; then
    echo "❌ frontend/package.json not found"
    exit 1
fi

echo "✅ Frontend package.json found"

# Check for environment variables
echo ""
echo "🔧 Environment Variables Required:"
echo "=================================="
echo "Backend (set in Render dashboard):"
echo "  - OPENAI_API_KEY"
echo "  - GOOGLE_API_KEY (if using Gemini)"
echo ""
echo "Frontend (set in render.yaml):"
echo "  - NEXT_PUBLIC_API_URL (will be set to backend URL)"
echo ""

# Push to repository
echo "📤 Pushing to repository..."
git add .
git commit -m "Deploy to Render - $(date)"
git push origin main

echo ""
echo "🎉 Deployment Preparation Complete!"
echo "=================================="
echo ""
echo "Next steps:"
echo "1. Go to https://dashboard.render.com"
echo "2. Click 'New +' → 'Blueprint'"
echo "3. Connect your repository"
echo "4. Set environment variables in Render dashboard"
echo "5. Deploy!"
echo ""
echo "Your services will be available at:"
echo "  - Backend: https://blackletter-backend.onrender.com"
echo "  - Frontend: https://blackletter-frontend.onrender.com"
echo ""
echo "Health check: https://blackletter-backend.onrender.com/health"
