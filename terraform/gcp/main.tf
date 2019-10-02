provider "google" {
  project = "stayapp-253702"
  region  = "australia-southeast1"
  zone    = "australia-southeast1-c"
}

provider "cloudflare" {
  version = "~> 2.0"
  email = "${var.cloudflare_email}"
  api_key = "${var.cloudflare_api_key}"
}

terraform {
  backend "gcs" {
    bucket = "stayapp-terraform-state"
    prefix = "terraform"
  }
}

module "compute" {
  source = "./modules/compute"
  tags   = "${var.tags}"
}

module "networking" {
  source = "./modules/networking"
  cloudflare_record_domain = "${var.cloudflare_record_domain}"
  cloudflare_record_name = "${var.cloudflare_record_name}"
}

module "sql" {
  source       = "./modules/sql"
  tags         = "${var.tags}"
  stayapp_ip = "${module.networking.stayapp_public_ip}"
  stayapp_sql_database_name = "${var.stayapp_sql_database_name}"
  sql_username = "${var.sql_username}"
  sql_password = "${var.sql_password}"
}
