resource "aws_ecr_repository" "ecr" {
  name = "${var.repository_name}"
  tags = "${var.tags}"
}

resource "aws_ecr_lifecycle_policy" "ecrpolicy" {
  repository = "${aws_ecr_repository.ecr.name}"

  policy = <<EOF
{
  "rules": [
    {
      "action": {
        "type": "expire"
      },
      "selection": {
        "countType": "imageCountMoreThan",
        "countNumber": 8,
        "tagStatus": "any"
      },
      "description": "Remove old images.",
      "rulePriority": 1
    }
  ]
}
  EOF
}