variable "ecr_name" {
  description = "Container registry name"
  type = "string"
}

variable "tags" {
  description = "Tags for all the resources"
  type = "map"
}
