# Cloud Computing Assigment Two

Real estate application using cloud resources

## Project name: Stay

Create a real estate helper tool by developing a simple web application that can fetch real estate data from the Domain real estate public API that can be displayed on Google maps. User session can be used to store saved locations and a cache can also be used to store external API data.

## Distributed model for the application

- Cluster computing
- Deploy PHP application -> fetches API data and potentially user session
- Use AWS EKS -> container orchestration

## Tools and techniques

- AWS -> cloud provider
- GitHub -> code repository
- GitLab or Azure DevOps -> CI/CI pipelines
- Terraform -> cloud deployment tool

## Data persistence

- MySQL server -> data persistence
- Redis server -> cache data (optional)
- GitLab container registry or AWS ECR -> Docker image storage

## User interface

- PHP application backend
- Vue.js frontend (optional)
- Grafana metrics dashboard (optional)
