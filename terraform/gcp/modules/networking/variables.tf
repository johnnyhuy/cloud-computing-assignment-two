variable "cloudflare_email" {
  description = "Cloudflare email used to auth against their API"
  type = "string"
}

variable "cloudflare_token" {
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
