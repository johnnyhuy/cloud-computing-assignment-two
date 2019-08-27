provider "google" {
  project     = "stayapp"
  region      = "australia-southeast1"
  zone        = "australia-southeast1-c"
}

terraform {
  backend "gcs" {
    bucket  = "stayapp"
    prefix  = "terraform.tfstate"
  }
}

module "compute" {
  source = "./modules/compute"
  tags = "${var.tags}"
}
