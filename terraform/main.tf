provider "aws" {
  version = "~> 2.0"
  region  = "ap-southeast-2"
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
