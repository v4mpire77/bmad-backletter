@echo off
REM Blackletter Systems - Render Deployment Script (Windows)
REM This script helps prepare and deploy the application to Render

echo 🚀 Blackletter Systems - Render Deployment
echo ==========================================

REM Check if git is initialized
if not exist ".git" (
    echo ❌ Git repository not found. Please initialize git first:
    echo    git init
    echo    git add .
    echo    git commit -m "Initial commit"
    pause
    exit /b 1
)

REM Check if remote is set
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo ⚠️  No remote repository found. Please add your GitHub repository:
    echo    git remote add origin https://github.com/yourusername/blackletter-systems.git
    echo    git push -u origin main
    pause
    exit /b 1
)

echo ✅ Git repository configured

REM Check if render.yaml exists
if not exist "render.yaml" (
    echo ❌ render.yaml not found. Please ensure the deployment configuration exists.
    pause
    exit /b 1
)

echo ✅ render.yaml found

REM Check backend requirements
if not exist "backend\requirements.txt" (
    echo ❌ backend\requirements.txt not found
    pause
    exit /b 1
)

echo ✅ Backend requirements found

REM Check frontend package.json
if not exist "frontend\package.json" (
    echo ❌ frontend\package.json not found
    pause
    exit /b 1
)

echo ✅ Frontend package.json found

REM Check for environment variables
echo.
echo 🔧 Environment Variables Required:
echo ==================================
echo Backend (set in Render dashboard):
echo   - OPENAI_API_KEY
echo   - GOOGLE_API_KEY (if using Gemini)
echo.
echo Frontend (set in render.yaml):
echo   - NEXT_PUBLIC_API_URL (will be set to backend URL)
echo.

REM Push to repository
echo 📤 Pushing to repository...
git add .
git commit -m "Deploy to Render - %date% %time%"
git push origin main

echo.
echo 🎉 Deployment Preparation Complete!
echo ==================================
echo.
echo Next steps:
echo 1. Go to https://dashboard.render.com
echo 2. Click "New +" → "Blueprint"
echo 3. Connect your repository
echo 4. Set environment variables in Render dashboard
echo 5. Deploy!
echo.
echo Your services will be available at:
echo   - Backend: https://blackletter-backend.onrender.com
echo   - Frontend: https://blackletter-frontend.onrender.com
echo.
echo Health check: https://blackletter-backend.onrender.com/health
echo.
pause

