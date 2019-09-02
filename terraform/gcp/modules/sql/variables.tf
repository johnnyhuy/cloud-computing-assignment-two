variable "tags" {
  description = "Tags for all the resources"
  type        = "map"
}

variable "sql_username" {
  description = "MySQL instance username"
  type        = "string"
}

variable "sql_password" {
  description = "MySQL instance password"
  type        = "string"
}
