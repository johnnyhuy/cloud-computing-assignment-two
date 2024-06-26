resource "google_sql_database_instance" "stayapp" {
  name   = "stayapp-sql-instance"
  region = "australia-southeast1"

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "kubernetes-stayapp-ip"
        value = "${var.stayapp_ip}"
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
  name     = "${var.stayapp_sql_database_name}"
  instance = "${google_sql_database_instance.stayapp.name}"
}
