@description('Location for all resources')
param location string = resourceGroup().location

@description('App Service Plan name')
param appServicePlanName string = 'blackletter-plan'

@description('Web App name')
param webAppName string = 'blackletter-web'

@description('API App name')
param apiAppName string = 'blackletter-api'

@description('SKU for the App Service Plan')
param sku string = 'B1'

// App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: sku
  }
  kind: 'linux'
  properties: {
    reserved: true
  }
}

// API App Service
resource apiApp 'Microsoft.Web/sites@2022-03-01' = {
  name: apiAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.11'
      appCommandLine: 'python -m uvicorn blackletter_api.main:app --host 0.0.0.0 --port 8000'
      appSettings: [
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'APP_ENV'
          value: 'prod'
        }
        {
          name: 'CORS_ORIGINS'
          value: 'https://${webAppName}.azurewebsites.net'
        }
      ]
    }
    httpsOnly: true
  }
}

// Web App Service
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'NODE|18-lts'
      appCommandLine: 'npm run start'
      appSettings: [
        {
          name: 'NEXT_PUBLIC_API_BASE'
          value: 'https://${apiApp.properties.defaultHostName}'
        }
        {
          name: 'NEXT_PUBLIC_USE_MOCKS'
          value: '0'
        }
        {
          name: 'SCM_DO_BUILD_DURING_DEPLOYMENT'
          value: 'true'
        }
        {
          name: 'WEBSITE_NODE_DEFAULT_VERSION'
          value: '18.x'
        }
      ]
    }
    httpsOnly: true
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output apiAppUrl string = 'https://${apiApp.properties.defaultHostName}'
