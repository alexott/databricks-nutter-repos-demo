This directory contains Terraform code to setup a Nutter demo project in the Azure DevOps.  To do that, you need to create a file `terraform.tfvars` with following variables:

* `devops_org_url`   - URL of your Azure DevOps instance, like, `https://dev.azure.com/company_name`.
* `devops_pat`       - Azure DevOps personal access token (PAT) obtained as described in [documentation](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/guides/authenticating_using_the_personal_access_token).  This PAT will be used to create a project in your Azure DevOps organization, and will be set inside Databricks workspace.
* `devops_user_name` - your user name inside Azure DevOps organization.

And then execute `terraform apply` (use `terraform plan` to understand what changes will be made).

The code performs following actions:

* Creates a new project inside Azure DevOps organization.  Default name is `NutterDemoProject` and could be changed by setting the `devops_project_name` variable.
* Creates a new Azure DevOps Git repository by cloning this demo.
* Set ups Git credential in Databricks workspace using provided Azure DevOps PAT.
* Creates 3 Databricks checkouts in the current user's folder with names `nutter-tf-dev`, `nutter-tf-staging`, and `nutter-tf-prod` to emulate transition between different stages.
* Creates a Databricks cluster that will be used to execute the tests.
* Creates a temporary Databricks Personal Access Token (PAT) that will be used to authenticate to Databricks workspace from the build pipeline.
* Creates an Azure DevOps variable group that contains all parameters that are used by the build pipeline.
* Creates an Azure DevOps build pipeline using `azure-pipelines.yaml` file from the cloned repository.

After code is executed, you will have fully configured repositories & build pipeline.  Follow instructions from the [top-level README](../../README.md) to setup release pipeline.


Limitations:

* This code doesn't setup release pipeline as no corresponding functionality is available.
