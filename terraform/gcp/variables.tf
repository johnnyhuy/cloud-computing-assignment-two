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

variable "cloudflare_api_token" {
  description = "Cloudflare token used to auth against their API"
  type = "string"
}

variable "cloudflare_record_domain" {
  description = "Cloudflare domain zone"
  type = "string"
}

variable "cloudflare_record_name" {
  description = "Cloudflare record name or subdomain"
  type = "string"
}
