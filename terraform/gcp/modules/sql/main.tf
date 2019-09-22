resource "google_sql_database_instance" "stayapp" {
  name   = "stayapp-sql"
  region = "australia-southeast1"

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "kubernetes-stayapp"
        value = "${var.cluster_service_ip_range}"
      }
      authorized_networks {
        name  = "allow-all"
        value = "0.0.0.0/0"
      }
    }
  }
}

resource "google_sql_user" "users" {
  name     = "${var.sql_username}"
  instance = "${google_sql_database_instance.stayapp.name}"
  host     = "%"
  password = "${var.sql_password}"
}

resource "google_sql_database" "database" {
  name     = "stayapp"
  instance = "${google_sql_database_instance.stayapp.name}"
}
