terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "eu-central-1"

  default_tags {
    tags = {
      Environment = "Production"
      Team        = "Data-Engineering"
      Owner       = "Zainab-Ojo"
      Managed_by  = "Terraform"
    }
  }
}