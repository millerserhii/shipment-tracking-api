variable "aws_region" {
  type        = string
  description = "AWS Region"
  default     = "eu-central-1"
}

variable "DB_USERNAME" {
  description = "The username for the RDS instance"
  type        = string
}

variable "DB_PASSWORD" {
  description = "The password for the RDS instance"
  type        = string
  sensitive   = true
}

variable "aws_cloudwatch_retention_in_days" {
  type        = number
  description = "AWS CloudWatch Logs Retention in Days"
  default     = 7
}

variable "app_name" {
  type        = string
  description = "aws-drf-boilerplate"
}

variable "app_environment" {
  type        = string
  description = "default environment"
  default     = "staging"
}

variable "cidr" {
  description = "The CIDR block for the VPC."
  default     = "10.0.0.0/16"
}

variable "public_subnets" {
  type        = list(string)
  description = "List of public subnets"
}

variable "private_subnets" {
  type        = list(string)
  description = "List of private subnets"
}

variable "availability_zones" {
  type        = list(string)
  description = "List of availability zones"
  default     = ["eu-central-1a", "eu-central-1b"]
}

variable "APP_CONTAINER_PORT" {
  description = "The port on which the app container listens"
  type        = number
  default     = 8000
}

variable "APP_HOST_PORT" {
  description = "The port on which the app host listens"
  type        = number
  default     = 8000
}
