resource "google_compute_address" "ip_address" {
  name = "stayapp-static-ip"
}

provider "cloudflare" {
  email = "${var.cloudflare_email}"
  token = "${var.cloudflare_token}"
}

resource "cloudflare_record" "single_a" {
  domain = "${var.cloudflare_record_domain}"
  name   = "${var.cloudflare_record_name}"
  value  = "${google_compute_address.ip_address.address}"
  type   = "A"
  ttl    = 3600
}
