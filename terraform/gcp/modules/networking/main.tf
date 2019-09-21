resource "google_compute_address" "ip_address" {
  name = "stayapp-static-ip"
}

resource "cloudflare_record" "single_a" {
  domain = "${var.cloudflare_record_domain}"
  name   = "${var.cloudflare_record_name}"
  value  = "${google_compute_address.ip_address.address}"
  type   = "A"
}
