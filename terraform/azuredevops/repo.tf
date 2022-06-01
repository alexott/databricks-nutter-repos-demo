data "databricks_current_user" "me" {
}

locals {
  staging_repo_path = "${data.databricks_current_user.me.repos}/nutter-tf-staging"
}

resource "databricks_git_credential" "global" {
  git_provider          = "azureDevOpsServices"
  git_username          = var.devops_user_name
  personal_access_token = var.devops_pat
  force                 = true
}

resource "databricks_repo" "nutter_in_user_home" {
  depends_on = [databricks_git_credential.global]
  url        = azuredevops_git_repository.repository.remote_url
  path       = "${data.databricks_current_user.me.repos}/nutter-tf-dev"
  branch     = "releases"
}

resource "databricks_repo" "nutter_in_staging" {
  depends_on = [databricks_git_credential.global]
  url        = azuredevops_git_repository.repository.remote_url
  path       = local.staging_repo_path
  branch     = "releases"
}

resource "databricks_repo" "nutter_in_prod" {
  depends_on = [databricks_git_credential.global]
  url        = azuredevops_git_repository.repository.remote_url
  path       = "${data.databricks_current_user.me.repos}/nutter-tf-prod"
  branch     = "releases"
}
