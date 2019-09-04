provider "google" {
  project = "stayapp"
  region  = "australia-southeast1"
  zone    = "australia-southeast1-c"
}

terraform {
  backend "gcs" {
    bucket = "stayapp-terraform"
    prefix = "terraform"
  }
}

module "compute" {
  source = "./modules/compute"
  tags   = "${var.tags}"
  service_account = "${var.service_account}"
}

module "sql" {
  source       = "./modules/sql"
  tags         = "${var.tags}"
  sql_username = "${var.sql_username}"
  sql_password = "${var.sql_password}"
}
