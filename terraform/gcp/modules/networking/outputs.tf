output "stayapp_public_ip" {
  value = "${google_compute_address.ip_address.address}"
}
