terraform {
  backend "s3" {
    bucket = "zainy-terraform-state-files"
    key    = "dev/dev.tfstate"
    region = "eu-central-1"
  }
}
