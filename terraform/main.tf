provider "aws" {
  version = "~> 2.0"
  region  = "ap-southeast-2"
}

resource "aws_ecr_repository" "foo" {
  name = "${var.ecr_name}-ecr"
}
