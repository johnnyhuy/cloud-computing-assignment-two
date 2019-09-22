variable "tags" {
  description = "Tags for all the resources"
  type        = "map"
}

variable "cluster_service_ip_range" {
  description = "The cluster IP range used to allow access to the database"
  type        = "string"
}

variable "sql_username" {
  description = "MySQL instance username"
  type        = "string"
}

variable "sql_password" {
  description = "MySQL instance password"
  type        = "string"
}
