// Azure Container Apps deployment for Blackletter app
@description('Location for all resources')
param location string = resourceGroup().location

@description('Environment name')
param environmentName string = 'blackletter-env'

@description('App name prefix')
param appNamePrefix string = 'blackletter'

@description('Container image tag')
param imageTag string = 'latest'

// Container Apps Environment
resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: environmentName
  location: location
  properties: {
    zoneRedundant: false
  }
}

// API Container App
resource apiContainerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${appNamePrefix}-api'
  location: location
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 8000
        allowInsecure: false
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
      }
      secrets: [
        {
          name: 'registry-password'
          value: 'your-registry-password' // Replace with your container registry password
        }
      ]
      registries: [
        {
          server: 'your-registry.azurecr.io' // Replace with your Azure Container Registry
          username: 'your-registry-username'
          passwordSecretRef: 'registry-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'api'
          image: 'your-registry.azurecr.io/${appNamePrefix}-api:${imageTag}'
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            {
              name: 'APP_ENV'
              value: 'prod'
            }
            {
              name: 'PORT'
              value: '8000'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
        rules: [
          {
            name: 'http-scaling'
            http: {
              metadata: {
                concurrentRequests: '10'
              }
            }
          }
        ]
      }
    }
  }
}

// Web Container App
resource webContainerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: '${appNamePrefix}-web'
  location: location
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      ingress: {
        external: true
        targetPort: 3000
        allowInsecure: false
        traffic: [
          {
            weight: 100
            latestRevision: true
          }
        ]
      }
      secrets: [
        {
          name: 'registry-password'
          value: 'your-registry-password'
        }
      ]
      registries: [
        {
          server: 'your-registry.azurecr.io'
          username: 'your-registry-username'
          passwordSecretRef: 'registry-password'
        }
      ]
    }
    template: {
      containers: [
        {
          name: 'web'
          image: 'your-registry.azurecr.io/${appNamePrefix}-web:${imageTag}'
          resources: {
            cpu: json('0.25')
            memory: '0.5Gi'
          }
          env: [
            {
              name: 'NEXT_PUBLIC_API_BASE'
              value: 'https://${apiContainerApp.properties.configuration.ingress.fqdn}'
            }
            {
              name: 'PORT'
              value: '3000'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 0
        maxReplicas: 3
      }
    }
  }
}

output webUrl string = 'https://${webContainerApp.properties.configuration.ingress.fqdn}'
output apiUrl string = 'https://${apiContainerApp.properties.configuration.ingress.fqdn}'
