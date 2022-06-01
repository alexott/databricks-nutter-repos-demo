resource "azuredevops_project" "project" {
  name            = var.devops_project_name
  description     = "Test Project for Nutter demo"
  visibility      = "private"
  version_control = "Git"
}

resource "azuredevops_git_repository" "repository" {
  project_id = azuredevops_project.project.id
  name       = "NutteronDevOps"
  initialization {
    init_type   = "Import"
    source_type = "Git"
    source_url  = "https://github.com/alexott/databricks-nutter-repos-demo"
  }
}

resource "azuredevops_build_definition" "build" {
  project_id = azuredevops_project.project.id
  name       = "Nutter Build Pipeline"

  ci_trigger {
    use_yaml = true
  }

  repository {
    repo_type   = "TfsGit"
    repo_id     = azuredevops_git_repository.repository.id
    branch_name = azuredevops_git_repository.repository.default_branch
    yml_path    = "azure-pipelines.yml"
  }

  variable_groups = [azuredevops_variable_group.vg.id]
}

resource "databricks_token" "pat_for_devops" {
  comment          = "Azure DevOps Nutter demo (10 days)"
  lifetime_seconds = 864000
}

resource "azuredevops_variable_group" "vg" {
  project_id   = azuredevops_project.project.id
  name         = "Nutter Testing"
  description  = "Variable group for build job"
  allow_access = true

  variable {
    name  = "databricks_host"
    value = data.databricks_current_user.me.workspace_url
  }

  variable {
    name         = "databricks_token"
    secret_value = databricks_token.pat_for_devops.token_value
    is_secret    = true
  }

  variable {
    name  = "cluster_id"
    value = databricks_cluster.nutter_demo.id
  }

  variable {
    name  = "staging_directory"
    value = local.staging_repo_path
  }

}
