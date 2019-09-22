output "mysql_server_ip" {
  value = "${module.sql.mysql_server_ip}"
}

output "cluster_ip" {
  value = "${module.compute.cluster_ip}"
}

output "cluster_service_ip_range" {
  value = "${module.compute.cluster_service_ip_range}"
}

output "cluster_version" {
  value = "${module.compute.cluster_version}"
}

output "stayapp_ip" {
  value = "${module.networking.stayapp_public_ip}"
}
