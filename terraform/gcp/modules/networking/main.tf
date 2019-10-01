resource "google_compute_address" "ip_address" {
  name = "stayapp-static-ip"
}

resource "cloudflare_zone" "stayapp_zone" {
    zone = "${var.cloudflare_record_domain}"
}

resource "cloudflare_record" "stayapp_record" {
  zone_id = "${cloudflare_zone.stayapp_zone.id}"
  name   = "${var.cloudflare_record_name}"
  value  = "${google_compute_address.ip_address.address}"
  type   = "A"
  ttl = 3600
}
