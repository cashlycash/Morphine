terraform {
  required_version = ">= 1.5.0"
}

variable "environment" {
  type    = string
  default = "dev"
}

output "note" {
  value = "Terraform scaffold for Morphine ${var.environment} environment"
}
