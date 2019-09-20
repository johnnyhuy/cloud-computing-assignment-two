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
}

module "networking" {
  source = "./modules/networking"
  cloudflare_email = "${var.cloudflare_email}"
  cloudflare_token = "${var.cloudflare_token}"
  cloudflare_record_domain = "${var.cloudflare_record_domain}"
  cloudflare_record_name = "${var.cloudflare_record_name}"
  cloudflare_record_ip_address = "${var.cloudflare_record_ip_address}"
}

module "sql" {
  source       = "./modules/sql"
  tags         = "${var.tags}"
  sql_username = "${var.sql_username}"
  sql_password = "${var.sql_password}"
}
