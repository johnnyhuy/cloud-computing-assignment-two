output "cluster_ip" {
  value = "${google_container_cluster.main.endpoint}"
}

output "cluster_service_ip_range" {
  value = "${google_container_cluster.main.services_ipv4_cidr}"
}

output "cluster_version" {
  value = "${google_container_cluster.main.master_version }"
}
