resource "aws_ecr_repository" "ecr" {
  name = "${var.repository_name}"
  tags = "${var.tags}"
}

resource "aws_ecr_lifecycle_policy" "ecrpolicy" {
  repository = "${aws_ecr_repository.ecr.name}"

  policy = <<EOF
{
  "rules": [
    {
      "action": {
        "type": "expire"
      },
      "selection": {
        "countType": "imageCountMoreThan",
        "countNumber": 4,
        "tagStatus": "any"
      },
      "description": "Remove old images.",
      "rulePriority": 1
    }
  ]
}
  EOF
}

resource "google_container_cluster" "primary" {
  name     = "stayapp"
  location = "australia-southeast1"
  remove_default_node_pool = true
  initial_node_count = 1

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "primary_preemptible_nodes" {
  name       = "stayapp-pool"
  location   = "australia-southeast1"
  cluster    = "${google_container_cluster.primary.name}"
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}