provider "google" {
  project = "${var.gcp_project_id}"
  region  = "australia-southeast1"
  zone    = "australia-southeast1-c"
}

provider "cloudflare" {
  email = "${var.cloudflare_email}"
  token = "${var.cloudflare_token}"
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
  cluster_ip = "${module.compute.cluster_ip}"
  sql_username = "${var.sql_username}"
  sql_password = "${var.sql_password}"
}
