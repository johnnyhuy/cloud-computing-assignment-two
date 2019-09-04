resource "google_container_cluster" "primary" {
  name                     = "stayapp"
  location                 = "australia-southeast1-a"
  min_master_version       = "1.13.7-gke.24"
  remove_default_node_pool = true
  initial_node_count       = 1

  node_config {
    service_account = "${var.service_account}"
  }

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
  location   = "australia-southeast1-a"
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
