variable "devops_org_url" {
  description = "DevOps URL"
  type        = string
}


variable "devops_pat" {
  description = "DevOps PAT"
  type        = string
}

variable "devops_user_name" {
  description = "DevOps User Name"
  type        = string
}

variable "devops_project_name" {
  description = "Project name in Azure DevOps"
  type        = string
  default     = "NutterDemoProject"
}
