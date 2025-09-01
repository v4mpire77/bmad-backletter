# 🚀 Render Deployment Checklist

## Pre-Deployment Checklist

### ✅ Repository Setup
- [ ] Git repository initialized
- [ ] Code pushed to GitHub/GitLab
- [ ] `render.yaml` file exists and is configured
- [ ] All files committed and pushed

### ✅ Backend Configuration
- [ ] `src/backend/requirements.txt` exists with all dependencies
- [ ] `src/backend/main.py` has proper CORS configuration
- [ ] Health check endpoint available (`/health`)
- [ ] Environment variables documented

### ✅ Frontend Configuration
- [ ] `frontend/package.json` exists with all dependencies
- [ ] `frontend/next.config.js` configured for web service
- [ ] API calls use environment variables
- [ ] Build script works locally

## Deployment Steps

### 1. Render Dashboard Setup
- [ ] Go to [Render Dashboard](https://dashboard.render.com)
- [ ] Sign up/Login with GitHub account
- [ ] Click "New +" → "Blueprint"
- [ ] Connect your repository

### 2. Environment Variables
- [ ] Set `OPENAI_API_KEY` in backend service
- [ ] Set `GOOGLE_API_KEY` in backend service (if using Gemini)
- [ ] Verify `NEXT_PUBLIC_API_URL` is set in frontend service

### 3. Deploy Services
- [ ] Backend service deploys successfully
- [ ] Frontend service deploys successfully
- [ ] Both services show "Live" status

### 4. Post-Deployment Verification
- [ ] Backend health check: `https://blackletter-backend.onrender.com/health`
- [ ] Frontend loads: `https://blackletter-frontend.onrender.com`
- [ ] API calls work from frontend to backend
- [ ] CORS errors resolved

## Troubleshooting

### Common Issues
- [ ] Build failures - check logs in Render dashboard
- [ ] CORS errors - verify frontend URL in backend CORS settings
- [ ] Environment variables - ensure all required keys are set
- [ ] Port issues - verify `$PORT` usage in start commands

### Quick Commands
```bash
# Check backend health
curl https://blackletter-backend.onrender.com/health

# Check frontend
curl https://blackletter-frontend.onrender.com

# View logs in Render dashboard
# Go to service → Logs tab
```

## Service URLs
- **Backend API**: `https://blackletter-backend.onrender.com`
- **Frontend**: `https://blackletter-frontend.onrender.com`
- **Health Check**: `https://blackletter-backend.onrender.com/health`

## Support
- [Render Documentation](https://render.com/docs)
- [Render Support](https://render.com/support)
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)

