terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=3.0.0"
    }
  }
}

# Configure the Microsoft Azure Provider
provider "azurerm" {
  features {}
  client_id       = "887ce85b-b289-42e7-a78d-1dbde039a0c8"
  client_secret   = var.client_secret
  tenant_id = "aa5fba84-fe75-490c-84db-382cd1342d45"
  subscription_id = "f93e2f54-a25c-4bdf-8a7e-8c9ce88553e5"
}