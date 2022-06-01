terraform {
  required_providers {
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = "0.2.1"
    }
    databricks = {
      source  = "databrickslabs/databricks"
      version = "0.5.8"
    }
  }
}

# https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs

provider "azuredevops" {
  org_service_url       = var.devops_org_url
  personal_access_token = var.devops_pat
}

provider "databricks" {
}
