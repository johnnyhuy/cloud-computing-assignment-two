data "null_data_source" "auth_netw_mysql_allowed" {
  count = 2

  inputs = {
    name  = "onprem-${count.index + 1}"
    value = "${element(list("35.244.76.200", "123.208.218.213"), count.index)}"
  }
}

resource "google_sql_database_instance" "stayapp" {
  name   = "stayapp-instance"
  region = "australia-southeast1"

  settings {
    tier = "db-f1-micro"

    ip_configuration {
      authorized_networks = [
        "${data.null_data_source.auth_netw_mysql_allowed.*.outputs}",
      ]
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
