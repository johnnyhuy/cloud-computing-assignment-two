# Cloud Computing Assignment Two

Real estate application using cloud resources

## Development

Here are the prerequisites:

- Docker

Yep that's it. Unless you want to run the Flask app on your host. Then you'll need to install Python. The Docker image should provide it's dependencies to run the application external from the host.

### Startup

Run the following command at the project root. We're using Docker Compose, a multi-container tool to run containers based on a single YAML config.

```bash
# Run the container from the Docker Compose config detached (-d)
docker-compose up -d
```

### How to stop development

Once you're done for the day, you can run the following command to stop all containers from that config.

```bash
docker-compose down
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
