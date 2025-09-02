# Deploy to Azure - Quick Guide

## Option 1: One-Click Azure Static Web Apps Deployment

[![Deploy to Azure](https://aka.ms/deploytoazurebutton)](https://portal.azure.com/#create/Microsoft.StaticApp)

### Steps:
1. Click the "Deploy to Azure" button above
2. Sign in to your Azure account
3. Fill in the deployment form:
   - **Subscription**: Choose your Azure subscription
   - **Resource Group**: Create new or use existing
   - **Name**: `blackletter-app`
   - **Region**: Choose closest to you
   - **Deployment Source**: GitHub
   - **GitHub Account**: Your GitHub account
   - **Organization**: `v4mpire77`
   - **Repository**: `bmad-backletter`
   - **Branch**: `main`
   - **Build Presets**: Next.js
   - **App Location**: `/apps/web`
   - **Api Location**: `/apps/api`
   - **Output Location**: `out`

4. Click "Review + Create" then "Create"

## Option 2: Azure Container Apps (Advanced)

If you prefer containerized deployment:

```bash
# Install Azure CLI (if not done)
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Login to Azure
az login

# Run deployment script
./deploy/azure/deploy-container-apps.sh
```

## Option 3: Manual Azure App Service

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a new "App Service"
3. Choose:
   - Runtime: Node 18 LTS
   - Region: Your preferred region
4. In deployment center, connect to your GitHub repo
5. Set build settings:
   - Build provider: GitHub Actions
   - Runtime: Node.js
   - Version: 18
   - Build command: `cd apps/web && npm install && npm run build`
   - Start command: `cd apps/web && npm start`

## Environment Variables to Set

In Azure portal, add these application settings:

```
NEXT_PUBLIC_API_BASE=https://your-api-url.azurewebsites.net
NEXT_PUBLIC_USE_MOCKS=0
NODE_ENV=production
WEBSITE_NODE_DEFAULT_VERSION=18.x
```

## Next Steps After Deployment

1. Your app will be available at the Azure-provided URL
2. Set up custom domain if needed
3. Configure SSL certificates
4. Set up monitoring and logging
5. Configure CI/CD pipeline for automatic deployments

## Troubleshooting

- Check deployment logs in Azure portal
- Verify all environment variables are set correctly
- Make sure Node.js version matches requirements
- Check that build outputs are in correct directory structure
