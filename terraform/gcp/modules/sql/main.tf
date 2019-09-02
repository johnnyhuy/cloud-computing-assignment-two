resource "google_sql_database_instance" "stayapp" {
  name   = "stayapp-instance"
  region = "australia-southeast1"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_user" "users" {
  name     = "${var.sql_username}"
  instance = "${google_sql_database_instance.stayapp.name}"
  host     = "${google_sql_database_instance.stayapp.host}"
  password = "${var.sql_password}"
}

resource "google_sql_database" "database" {
  name     = "stayapp"
  instance = "${google_sql_database_instance.stayapp.name}"
}
