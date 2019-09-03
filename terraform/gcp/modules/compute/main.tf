resource "google_container_cluster" "stayapp-austse" {
  name                     = "stayapp-austse"
  location                 = "australia-southeast1"
  min_master_version       = "1.13.7-gke.24"
  remove_default_node_pool = true
  initial_node_count       = 1

  node_config {
    tags = ["education", "region-austse"]
  }

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_cluster" "stayapp-us" {
  name                     = "stayapp-us"
  location                 = "us-east4"
  min_master_version       = "1.13.7-gke.24"
  remove_default_node_pool = true
  initial_node_count       = 1

  node_config {
    tags = ["region-us"]
  }

  master_auth {
    username = ""
    password = ""

    client_certificate_config {
      issue_client_certificate = false
    }
  }
}

resource "google_container_node_pool" "stayapp-austse-pool" {
  name       = "stayapp-pool"
  cluster    = "${google_container_cluster.stayapp-austse.name}"
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    tags = ["region-austse"]

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}

resource "google_container_node_pool" "stayapp-us-pool" {
  name       = "stayapp-pool-us"
  cluster    = "${google_container_cluster.stayapp-us.name}"
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    tags = ["region-us"]

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}

resource "google_compute_address" "ip_address" {
  name = "stayapp-static-ip"
}

provider "acme" {
  server_url = "https://acme-staging-v02.api.letsencrypt.org/directory"
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "acme_registration" "reg" {
  account_key_pem = "${tls_private_key.private_key.private_key_pem}"
  email_address   = "info@johnnyhuy.com"
}

resource "acme_certificate" "johnnyhuy_acme" {
  account_key_pem           = "${acme_registration.reg.account_key_pem}"
  common_name               = "johnnyhuy.com"
  subject_alternative_names = ["stay.johnnyhuy.com"]

  dns_challenge {
    provider = "cloudflare"

    config = {
      CF_API_EMAIL = "johnnyhuynhdev@gmail.com"
      CF_API_KEY   = "172ffc049e23a2cb8fb63b15fa29aca547b5a"
    }
  }
}

resource "google_compute_ssl_certificate" "johnnyhuy_certificate" {
  name        = "johnnyhuy-certificate"
  private_key = "${acme_certificate.johnnyhuy_acme.private_key_pem}"
  certificate = "${acme_certificate.johnnyhuy_acme.certificate_pem}${acme_certificate.johnnyhuy_acme.issuer_pem}"

  lifecycle {
    create_before_destroy = true
  }
}

# resource "google_compute_global_address" "default" {
#   name         = "stayapp-global-ip"
#   ip_version   = "IPV4"
#   address_type = "EXTERNAL"
# }

# resource "google_compute_target_http_proxy" "http" {
#   count   = 1
#   name    = "${var.name}-http-proxy"
#   url_map = var.url_map
# }

# resource "google_compute_global_forwarding_rule" "http" {
#   provider   = google-beta
#   count      = 1
#   name       = "${var.name}-http-rule"
#   target     = google_compute_target_http_proxy.http[0].self_link
#   ip_address = google_compute_global_address.default.address
#   port_range = "80"

#   depends_on = [google_compute_global_address.default]

#   labels = var.custom_labels
# }
