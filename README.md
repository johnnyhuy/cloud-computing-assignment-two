# Cloud Computing Assignment Two

Real estate application using cloud resources

- [Cloud Computing Assignment Two](#cloud-computing-assignment-two)
  - [Application Development](#application-development)
    - [Startup Flask app](#startup-flask-app)
    - [How to stop Flask app](#how-to-stop-flask-app)
  - [Infrastructure Development](#infrastructure-development)
    - [How to run a deployment from you local machine](#how-to-run-a-deployment-from-you-local-machine)
  - [Project name: Stay](#project-name-stay)
    - [Distributed model for the application](#distributed-model-for-the-application)
    - [Tools and techniques](#tools-and-techniques)
    - [Data persistence](#data-persistence)
    - [User interface](#user-interface)
    - [Layout](#layout)

## Application Development

Here are the prerequisites:

- Docker

Yep that's it. Unless you want to run the Flask app on your host. Then you'll need to install Python. The Docker image should provide it's dependencies to run the application external from the host.

### Startup Flask app

Run the following command at the project root. We're using Docker Compose, a multi-container tool to run containers based on a single YAML config.

```bash
# Run the container from the Docker Compose config detached (-d)
docker-compose up -d
```

### How to stop Flask app

Once you're done for the day, you can run the following command to stop all containers from that config. Make sure you're in the root project directory.

```bash
# Remove all running containers
docker-compose down
```

## Infrastructure Development

We're currently using Terraform to deploy our infrastructure stored as code. Using a pipeline from Azure DevOps we can leverage a code change to deploy infrastructure automatically.

Here's a list of infrastructure files and folders involved:

- `terraform/` - templates to deploy cloud resources to AWS
- `pipelines/infrastructure.yml` - the infrastructure deployment pipeline

Here are the prerequisites to start work on it:

- Terraform CLI
- AWS CLI
- GCloud SDK

[Terraform Getting started - AWS](https://learn.hashicorp.com/terraform/getting-started/install)

### How to run a deployment from you local machine

Sometimes we don't need to leverage the pipelines to deploy things into the cloud.

Here's some quick start commands to deploy the resources from your local machine. Change directory to the **project root** and run the following commands.

```bash
# Initialise Terraform modules in the folder
terraform init

# Dry run deploy the resource
terraform plan

# Deploy the resources
terraform apply
```

## Project name: Stay

Create a real estate helper tool by developing a simple web application that can fetch real estate data from the Domain real estate public API that can be displayed on Google maps. User session can be used to store saved locations and a cache can also be used to store external API data.

### Distributed model for the application

- Cluster computing
- Deploy PHP application -> fetches API data and potentially user session
- Use AWS EKS -> container orchestration

### Tools and techniques

- AWS -> cloud provider
- GitHub -> code repository
- GitLab or Azure DevOps -> CI/CI pipelines
- Terraform -> cloud deployment tool

### Data persistence

- MySQL server -> data persistence
- Redis server -> cache data (optional)
- GitLab container registry or AWS ECR -> Docker image storage

### User interface

- PHP application backend
- Vue.js frontend (optional)
- Grafana metrics dashboard (optional)

### Layout

This is the application layout of the Python application in a Kubernetes cluster.

![application](./images/cloud-computing-design-application.png)

This is the continuous integration and delivery process to get it into the cloud.

![ci-cd](./images/cloud-computing-design-ci-cd.png)