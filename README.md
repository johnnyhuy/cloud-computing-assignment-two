# Cloud Computing Assignment Two

Real estate application using cloud resources for RMIT Cloud Computing course semester 2 2019.

- [Cloud Computing Assignment Two](#cloud-computing-assignment-two)
  - [Project name: Stay App](#project-name-stay-app)
    - [Distributed model for the application](#distributed-model-for-the-application)
    - [Tools and techniques](#tools-and-techniques)
    - [Data persistence](#data-persistence)
    - [User interface](#user-interface)
    - [Layout](#layout)
  - [Application Development](#application-development)
    - [Startup Fast API app](#startup-fast-api-app)
    - [How to stop Fast API app](#how-to-stop-fast-api-app)
  - [Infrastructure Development](#infrastructure-development)
    - [(Optional) How to run a deployment from you local machine](#optional-how-to-run-a-deployment-from-you-local-machine)
  - [Azure DevOps deployment](#azure-devops-deployment)
    - [Requirements](#requirements)
    - [Creating the project](#creating-the-project)
    - [Creating the pipelines](#creating-the-pipelines)
    - [Get the application pipeline deploying applications](#get-the-application-pipeline-deploying-applications)
      - [AWS extension](#aws-extension)
      - [Terraform extension](#terraform-extension)
      - [Kubernetes extension](#kubernetes-extension)
    - [Run the bloody pipelines!](#run-the-bloody-pipelines)

## Project name: Stay App

Create a real estate helper tool by developing a simple web application that can fetch real estate data from the Domain real estate public API that can be displayed on Google maps. User session can be used to store saved locations and a cache can also be used to store external API data.

**Disclaimer:** this application requires GCP and AWS hosting, which costs money. The [stay.johnnyhuy.com](https://stay.johnnyhuy.com) demo link to the application may not exist as time passes. The application can be launched from the ground up with **Terraform**.

![](images/2019-10-05-09-35-43.png)

![](images/2019-10-05-09-36-04.png)

![](images/2019-10-05-09-36-23.png)

### Distributed model for the application

- Cluster computing -> Google Kubernetes Engine as the container orchestration tool
- Deploy Python application -> fetches API data and call a cloud database

### Tools and techniques

- [Google Cloud Platform](https://cloud.google.com/) -> cloud provider
- [Amazon Web Services](https://aws.amazon.com/?nc2=h_lg) -> secondary cloud provider
- [GitHub](https://github.com/) -> code repository
- [Azure DevOps](https://dev.azure.com/) -> DevOps pipelines
- [Terraform](https://www.terraform.io/) -> cloud deployment tool

### Data persistence

- [MySQL server](https://cloud.google.com/sql/docs/mysql/) -> data persistence of crime data and pricing
- [Amazon ECR](https://aws.amazon.com/ecr/) -> Docker image storage

### User interface

- Python [Fast API](https://github.com/tiangolo/fastapi) + [Jinja templating](https://jinja.palletsprojects.com/en/2.10.x/)

### Layout

This is the application layout of the Python application in a Kubernetes cluster.

![application](./images/cloud-computing-design-application-update.png)

This is the continuous integration and delivery process to get it into the cloud.

![ci-cd](./images/cloud-computing-design-ci-cd-update.png)

## Application Development

We've provided a easy local development experience by using [Docker](https://www.docker.com/) to produce a consistent environment on any development system.

### Startup Fast API app

Run the following command at the project root. We're using [Docker Compose](https://docs.docker.com/compose/), a multi-container tool to run containers based on a single YAML config.

```bash
# Run the container from the Docker Compose config detached (-d)
docker-compose up -d --build
```

### How to stop Fast API app

Once you're done for the day, you can run the following command to stop all containers from that config. Make sure you're in the root project directory.

```bash
# Remove all running containers
docker-compose down
```

## Infrastructure Development

We're currently using [Terraform](https://www.terraform.io/) to deploy our infrastructure stored as code. Using a pipeline from Azure DevOps we can leverage a code change to deploy infrastructure with full automation.

Here's a list of infrastructure files and folders involved:

- `terraform/` - templates used to deploy cloud resources
- `pipelines/infrastructure.yml` - the infrastructure deployment pipeline for Azure DevOps

Here are the prerequisites to start work on it:

- [Terraform CLI](https://learn.hashicorp.com/terraform/getting-started/install.html)
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
- [GCloud SDK](https://cloud.google.com/sdk/install)

[Terraform Getting started - AWS](https://learn.hashicorp.com/terraform/getting-started/install)

### (Optional) How to run a deployment from you local machine

Sometimes we don't need to leverage Azure DevOps pipelines to deploy things into the cloud. Though this comes with the trade-off of more manual steps including getting the cloud provider credentials for Terraform to use.

Here's some quick start commands to deploy the resources from your local machine. Change directory to either `terraform/gcp` or `terraform/aws` and run the following command to deploy resources. Be sure to have relevant Cloud credentials installed on the local machine before continuing.

```bash
# Initialise Terraform modules in the folder
terraform init

# Dry run deploy the resource
terraform plan

# Deploy the resources
terraform apply
```

## Azure DevOps deployment

This section will cover the setup in Azure DevOps

### Requirements

- Google Cloud Platform account
- Amazon Web Services account
- Azure DevOps account
- CloudFlare account
- A custom domain with access to its DNS records

### Creating the project

- Go to [Azure DevOps](dev.azure.com) and login with a Microsoft account
- Create a Azure DevOps project
- Install the following Azure DevOps extensions on the organisation

![](images/2019-10-05-09-39-42.png)

- Setup the following service connections (we will create the Kubernetes service connection later)

![](images/2019-10-05-09-38-10.png)

### Creating the pipelines

- Go to the Azure DevOps project and navigate to the Pipelines page and create an existing pipeline
- Link the existing pipeline to the GitHub repository

![](images/2019-10-05-09-41-27.png)

- There are two pipelines to add and rename them accordingly
  - `pipelines/application.yml`
  - `pipelines/infrastructure.yml`
- Create a variables group with the following values

![](images/2019-10-05-09-52-43.png)

### Get the application pipeline deploying applications

Pipelines are set in the code repository under `pipelines/application.yml` and `pipelines/infrastructure.yml` to allow Azure DevOps to run against their build agents.

![](images/2019-09-21-08-57-17.png)

We have installed the following Azure DevOps extensions under the organization:

- [AWS Tools for Microsoft Visual Studio Team Services by Amazon Web Services](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.aws-vsts-tools)
- [Terraform by Microsoft DevLabs](https://marketplace.visualstudio.com/items?itemName=ms-devlabs.custom-terraform-tasks)

The infrastructure pipeline is the **initial** pipeline used to create the *underlying cloud resources* for the **application pipeline** to deploy on on top. We needed to setup individual service connections in order to allow the pipelines in Azure DevOps talk to cloud providers.

Service connection list required for the infrastructure and application pipelines based of specific extensions:

#### AWS extension

- aws-service-connection

#### Terraform extension

- aws-terraform-service-connection
- google-terraform-service-connection

#### Kubernetes extension

- gcp-gke-service-connection

Run the infrastructure pipeline first and get access into the newly created Kubernetes cluster by running the following commands to create a service account in the cluster (this is a tricky manual task).

```bash
# Login to GCloud
gcloud auth login

# Get the cluster credentials, replace the brackets accordingly
gcloud container clusters get-credentials [GKE cluster name] --region [region of the cluster]
```

We need a service account for the Azure DevOps service connection to allow the application pipeline to talk to the cluster.

```bash
# Deploy the service account based on a config in this repository
# Be sure you're in the root directory of this repository
kubectl apply ./init

# Get the secret value of the service account
kubectl describe sa 'stayapp-serviceaccount'

# Use the the first token name from the previous output of the command
# Copy the output of this command
kubectl get secret -o yaml [service account token name]
```

Create a service connection in the Azure DevOps "Settings > Service connections" and choose the "Kubernetes" option.

![](images/2019-09-21-08-38-50.png)

Should be greeted with a menu to create a Kubernetes service connection.

- **Connection name:** gcp-service-connection
- **Service URL:** "get the cluster IP from GCloud Console"
- **Secret:** "use the output of the `kubectl get secret`"

Now we can use both the infrastructure and application pipelines to deploy our cloud resources and application on top.

### Run the bloody pipelines!

Hopefully everything is working by now. We can run the **infrastructure** pipeline to create cloud infrastructure.

Once we have cloud resources deployed, go to the GCP console and find the public static IP produced by the infrastructure pipeline. Modify the `loadBalancerIP` field at `kubernetes/stayapp/service.yml` to the IP address accordingly. Push the code up and deploy the application pipeline based off that branch with the change.
