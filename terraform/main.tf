provider "aws" {
  version = "~> 2.0"
  region  = "ap-southeast-2"
}

provider "google" {
  project     = "stayapp"
  region      = "australia-southeast1"
  zone        = "australia-southeast1-c"
}

terraform {
  backend "s3" {
    bucket = "stayapp-terraform"
    key    = "terraform"
    region = "ap-southeast-2"
  }
}

module "compute" {
  source = "./modules/compute"
  repository_name = "${var.repository_name}"
  tags = "${var.tags}"
}
