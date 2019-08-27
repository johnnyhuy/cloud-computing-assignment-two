provider "google" {
  project = "stayapp"
  region  = "australia-southeast1"
  zone    = "australia-southeast1-c"
}

terraform {
  backend "gcs" {
    bucket  = "stayapp-terraform"
  }
}

module "compute" {
  source = "./modules/compute"
  tags   = "${var.tags}"
}
