output "mysql_server_ip" {
  value = "${google_sql_database_instance.stayapp.public_ip_address}"
}
