This repository contains notebooks & instructions for setting up the demo of development workflow & CI/CD (on Azure DevOps) using the Databricks notebooks and [Repos feature](https://docs.databricks.com/repos.html).  Testing of notebooks is done using the [Nutter library](https://github.com/microsoft/nutter) developed by Microsoft.  

Two approaches are demonstrated:
1. Using notebooks & including the code using `%run` ([doc](https://docs.databricks.com/notebooks/notebooks-use.html#run)) - the "main" code is in the notebooks `Code1.py` and `Code2.py`, and the testing code is in the `unit-tests/test_with_percent_run.py`.
1. Using notebook for test itself, but including main code as Python packages using [arbitrary files in Repos](https://docs.databricks.com/repos.html#work-with-non-notebook-files-in-a-databricks-repo) functionality (DBR 9.1+).  Main code is in the `my_package/code1.py` and `my_package/code2.py` files, and test is in `unit-tests/test_with_arbitrary_files.py`.

This demo shows how you can use Repos to work on your own copy of notebooks, test them after commit in the "staging" environment, and promote to "production" on successful testing of `releases` branch.

# The workflow

The development workflow is organized as on following image:

![Development workflow](images/cicd-workflow.png)

1. Developer works on the code in the separate environment (personal space on Databricks, etc.).  When code changes are done, they are committed into some branch
1. CI/CD implementation (Azure DevOps here) picks up the changes, and tests them in a staging environment (executes the "build pipeline").  This consists of several steps (see [azure-pipelines.yml](azure-pipelines.yml) for technical details):
   * Update repository checkout in the "Staging" folder
   * Execute tests with updated code
   * Publish tests results
1. In current setup, there are different jobs for the "normal" branches, and for "release" branch (`releases` in this setup), this would allow to run different sets of tests when we're preparing the release
1. If commit is done to the "release branch, and there are no test failures, then the "release pipeline" is triggered, and it updates the production environment by updating the repository checkout in the "Production" folder.


# Setup on Databricks side

Your Databricks workspace needs to have Repos functionality enabled.  If it's enabled, you should see the "Repos" icon in the navigation panel:

* Fork repository into your environment - Github, or Azure DevOps (follow Databricks documentation on using it)
* In the Repos, click "Create Repo" and link it to the Git repository that you've forked - this will be your personal copy of the code that will be used for work:

![Create a personal repo](images/create-personal-project.png)

* Create the staging & production checkouts
  * In the Repos, in the top-level part, click on the "ᐯ" near the "Repos" header, select "Create" and select "Folder" (see image).  Give it the name "Staging":

![Create a staging folder](images/create-staging-folder.png)

  * Click on the  "ᐯ" near the "Staging" folder, and click "Create" and select "Repo":

![Create a staging repository](images/create-project-in-staging.png)

  * Link it to the Git repository, similarly how you did it for your personal checkout
  * Create the "Production" folder with repository inside, repeating two previous steps
* Create a new cluster that will be used for execution of the tests, you will need to pass the [cluster ID](https://docs.databricks.com/workspace/workspace-details.html#cluster-url-and-id) to the Nutter to execute the tests


# Setup Azure DevOps pipelines

The Azure DevOps setup consists of the several steps, described in the next sections.  It's assumed that project in Azure DevOps already exists.

We need to create a [personal access token (PAT)](https://docs.databricks.com/administration-guide/access-control/tokens.html) that will be used for execution of the tests & updating the repository.  This token will be used to authenticate to Databricks workspace, and then it will fetch configured token to authenticate to Git provider.  We also need to connect Databricks workspace to the Git provider - usually it's done by using the provider-specific access tokens - see [documentation](https://docs.databricks.com/repos.html#configure-your-git-integration-with-databricks) on details of setting the integration with specific Git provider (**note, that when repository is on Azure DevOps, you still need to generate Azure DevOps token to make API working**!, and also provide the user name in the Git settings). 

> :warning: the previous instructions on using Repos + Azure DevOps with service principals weren't correct, so were removed!

### Create variables group to keep common configuration

Because we have several pipelines, the it's makes sense to define [variable group](https://docs.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups) to store the data that are necessary for execution of tests & deployment of the code.  We need following configuration properties for execution of our pipelines:

* `databricks_host` - the [URL of your workspace](https://docs.databricks.com/workspace/workspace-details.html#workspace-instance-names-urls-and-ids) where tests will be executed (host name with `https://`, without `?o=`, and without trailing slash character.  For example: `https://adb-1568830229861029.9.azuredatabricks.net`).
* `databricks_token` - personal access token for executing commands against the workspace.  Mark this variable as private!  Note that if you're using Azure DevOps to host repository, then you need to use AAD token instead (see instructions below).
* `cluster_id` - the ID of the cluster where tests will be executed. DBR 9.1+ should be used to support arbitrary files.
* `staging_directory` - the directory for staging checkout that we created above. For example, `/Repos/Staging/databricks-nutter-projects-demo`.

The name of the variable group is used in the [azure-pipelines.yml](azure-pipelines.yml). By default its name is "Nutter Testing".  Change the [azure-pipelines.yml](azure-pipelines.yml) if you use another name for variable group.

### Create a build pipeline

Azure DevOps can work with GitHub repositories as well - see [documentation](https://docs.microsoft.com/en-us/azure/devops/pipelines/repos/github) for more details on how to link DevOps with GitHub.

* In the Azure DevOps, in the Pipelines section, select Pipelines, and click "New pipeline"
* Select GitHub and repository
* In the "Configure" step select the "Existing Azure Pipelines YAML file" and specify the name of the existing file: [azure-pipelines.yml](azure-pipelines.yml)
* Save pipeline


### Create a release pipeline

* In the Azure DevOps, in the Pipelines section, select Releases, and click "New release pipeline"
* Select "Empty Job" in the dialog
* In the Stage dialog enter some meaningful name for it
* In the "Variables" tab, link the variable group that was created previously
* Configure job & task:
  * Configure agent - in the "Agent Specification" select "ubuntu-18.04"
  * Click on "+" and find the "Command line" task
  * Enter following code that will connect to the production environment & update the checkout of the repository (via [Repos REST API](https://docs.databricks.com/dev-tools/api/latest/repos.html)):

```sh
python -m pip install --upgrade databricks-cli
databricks repos update --path /Repos/Production/databricks-nutter-projects-demo --branch releases
```

  * Below the code, add environment variable `DATABRICKS_TOKEN` with value `$(DATABRICKS_TOKEN)` - this will pull it from the variable group into the script's execution context
  * Save task & job
* We also need to configure an artifact:
  * Click on "Add artifact", select project, and source (the name of the build pipeline). Also, for "Default version" select "Latest from specific branch with tags" and select the "releases" branch.  Click on "Add" to add artifact into pipeline
  * Click on the "⚡" icon to configure the continuous deployment (by default, release is triggered manually).  Add branch filter and also select the `releases` branch
* Your release pipeline should look as following:

![Release pipeline](images/release-pipeline.png)

* Save the pipeline

After all of this done, the release pipeline will be automatically executed on every successful build in the `releases` branch.
