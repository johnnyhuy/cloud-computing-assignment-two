resource "google_container_cluster" "main" {
  name                     = "stayapp-cluster"
  location                 = "australia-southeast1-a"
  min_master_version       = "1.13.9-gke.3"
  remove_default_node_pool = true
  initial_node_count       = 1

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "node" {
  name       = "stayapp-node-pool"
  location   = "australia-southeast1-a"
  cluster    = "${google_container_cluster.main.name}"
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
