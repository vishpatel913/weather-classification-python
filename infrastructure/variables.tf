variable "app_name" {
  description = "Application name"
  type        = string
  default     = "t-shirt-weather-api"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}