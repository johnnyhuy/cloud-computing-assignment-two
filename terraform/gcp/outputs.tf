output "mysql_server_ip" {
  value = "${module.sql.mysql_server_ip}"
}

output "cluster_ip" {
  value = "${module.compute.cluster_ip}"
}

output "stayapp_ip" {
  value = "${module.networking.stayapp_public_ip}"
}
