resource "google_container_cluster" "stayapp_austse_cluster" {
  name                     = "stayapp-austse"
  location                 = "australia-southeast1"
  min_master_version       = "1.13.7-gke.24"
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

resource "google_container_cluster" "stayapp_us_cluster" {
  name     = "stayapp-us"
  location = "us-east4"
  min_master_version       = "1.13.7-gke.24"
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

resource "google_container_node_pool" "stayapp_austse_pool" {
  name       = "stayapp-pool"
  cluster    = "${google_container_cluster.stayapp-austse.name}"
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    tags         = ["region-austse"]

    metadata = {
      disable-legacy-endpoints = "true"
    }

    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]
  }
}

resource "google_container_node_pool" "stayapp_us_pool" {
  name       = "stayapp-pool-us"
  cluster    = "${google_container_cluster.stayapp-us.name}"
  node_count = 1

  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    tags         = ["region-us"]

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
      CF_API_KEY   = "05c3066e319ab980ed7df4ab1fef2a0b22b91"
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

resource "google_compute_global_address" "stayapp_global_address" {
  name         = "stayapp-global-ip"
  ip_version   = "IPV4"
  address_type = "EXTERNAL"
}

resource "google_compute_global_forwarding_rule" "stayapp_https" {
  count      = 1
  name       = "stayapp-https-rule"
  target     = google_compute_target_https_proxy.stayapp_https_proxy[0].self_link
  ip_address = "${google_compute_global_address.stayapp_global_address.address}"
  port_range = "443"
  depends_on = [google_compute_global_address.stayapp_global_address]
}

resource "google_compute_target_https_proxy" "stayapp_https_proxy" {
  count   = 1
  name    = "stayapp-https-proxy"
  url_map = "${google_compute_url_map.stayapp_url_map.self_link}"

  ssl_certificates = ["${google_compute_ssl_certificate.johnnyhuy_certificate.self_link}"]
}

resource "google_compute_url_map" "stayapp_url_map" {
  name        = "stayapp-url-map"

  default_service = "${google_compute_backend_service.stayapp_backend.self_link}"

  host_rule {
    hosts        = ["stay.johnnyhuy.com"]
    path_matcher = "allpaths"
  }

  path_matcher {
    name            = "allpaths"
    default_service = "${google_compute_backend_service.stayapp_backend.self_link}"

    path_rule {
      paths   = ["/*"]
      service = "${google_compute_backend_service.stayapp_backend.self_link}"
    }
  }
}

resource "google_compute_backend_service" "stayapp_backend" {
  name        = "stayapp-backend"
  port_name   = "http"
  protocol    = "HTTP"
  timeout_sec = 10

  health_checks = ["${google_compute_http_health_check.stayapp_health_check.self_link}"]
}

resource "google_compute_http_health_check" "stayapp_health_check" {
  name               = "stayapp-health-check"
  request_path       = "/"
  check_interval_sec = 1
  timeout_sec        = 1
}
