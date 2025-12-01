targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment (used for naming resources)')
param environmentName string

@description('Name of the resource group')
param resourceGroupName string = 'rg-${environmentName}'

@description('Location for all resources')
param location string = 'eastus2'

@description('ACR SKU')
@allowed(['Basic', 'Standard', 'Premium'])
param acrSku string = 'Basic'

// Unique suffix for globally unique names
var uniqueSuffix = uniqueString(subscription().subscriptionId, resourceGroupName)
// ACR names must be alphanumeric only (no hyphens), 5-50 chars
var sanitizedEnvName = replace(environmentName, '-', '')
var acrName = 'cr${sanitizedEnvName}${uniqueSuffix}'

// Tags
var tags = {
  'azd-env-name': environmentName
}

// Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2024-03-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// Azure Container Registry (inline)
module acr 'acr.bicep' = {
  name: 'acr-deployment'
  scope: rg
  params: {
    acrName: acrName
    location: location
    sku: acrSku
    tags: tags
  }
}

// Outputs for azd to consume
output AZURE_CONTAINER_REGISTRY_NAME string = acr.outputs.acrName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = acr.outputs.acrLoginServer
output AZURE_RESOURCE_GROUP string = rg.name
