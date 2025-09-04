#!/bin/bash

# Azure Container Apps Deployment Script
# This script deploys your Blackletter app to Azure Container Apps

set -e

# Configuration
RESOURCE_GROUP="blackletter-rg"
LOCATION="eastus"
ACR_NAME="blackletteracr"
APP_NAME="blackletter"

echo "🚀 Starting Azure Container Apps deployment..."

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo "❌ Azure CLI is not installed. Please install it first:"
    echo "https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Login to Azure (if not already logged in)
echo "🔐 Checking Azure login status..."
if ! az account show &> /dev/null; then
    echo "Please login to Azure:"
    az login
fi

# Create resource group
echo "📦 Creating resource group..."
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
echo "📋 Creating Azure Container Registry..."
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Get ACR login server
ACR_SERVER=$(az acr show --name $ACR_NAME --resource-group $RESOURCE_GROUP --query loginServer --output tsv)
echo "🏗️ ACR Server: $ACR_SERVER"

# Get ACR credentials
ACR_USERNAME=$(az acr credential show --name $ACR_NAME --query username --output tsv)
ACR_PASSWORD=$(az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv)

# Login to ACR
echo "🔑 Logging into Azure Container Registry..."
echo $ACR_PASSWORD | docker login $ACR_SERVER --username $ACR_USERNAME --password-stdin

# Build and push the container image
echo "🏗️ Building and pushing container image..."
docker build -t $ACR_SERVER/$APP_NAME:latest -f deploy/docker/Dockerfile .
docker push $ACR_SERVER/$APP_NAME:latest

# Install Container Apps extension
echo "🔧 Installing Container Apps extension..."
az extension add --name containerapp --upgrade

# Register providers
echo "📝 Registering providers..."
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

# Replace registry placeholders in the Bicep template so it references the pushed image
echo "📋 Updating Bicep template with registry credentials..."
sed -i "s/your-registry.azurecr.io/$ACR_SERVER/g" deploy/azure/container-apps.bicep
sed -i "s/your-registry-username/$ACR_USERNAME/g" deploy/azure/container-apps.bicep
sed -i "s/your-registry-password/$ACR_PASSWORD/g" deploy/azure/container-apps.bicep

# Deploy using Bicep template
echo "🚀 Deploying to Azure Container Apps..."
az deployment group create \
    --resource-group $RESOURCE_GROUP \
    --name container-apps \
    --template-file deploy/azure/container-apps.bicep \
    --parameters \
        appNamePrefix=$APP_NAME \
        imageTag=latest

# Get the deployment outputs
WEB_URL=$(az deployment group show --resource-group $RESOURCE_GROUP --name container-apps --query properties.outputs.webUrl.value --output tsv)
API_URL=$(az deployment group show --resource-group $RESOURCE_GROUP --name container-apps --query properties.outputs.apiUrl.value --output tsv)

echo "✅ Deployment complete!"
echo "🌐 Web App URL: $WEB_URL"
echo "🔗 API URL: $API_URL"

echo "📋 Next steps:"
echo "1. Test your application at: $WEB_URL"
echo "2. Set up custom domain if needed"
echo "3. Configure environment variables in Azure Portal"
echo "4. Set up monitoring and logging"
