provider "aws" {
  region = var.region
}

terraform {
  required_version = ">= 0.13"

  backend "s3" {
    bucket = "sbb-remote-state"
    key    = "terraform.tfstate"
    region = "eu-west-3"
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.19.0"
    }
    template = {
      source  = "hashicorp/template"
      version = "~> 2.2.0"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0.0"
    }
  }
}