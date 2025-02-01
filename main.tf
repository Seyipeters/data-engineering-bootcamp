terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.5.0"
    }
  }
}

provider "google" {
  project = "annular-system-367502"
  region = "us-central1"
}

resource "google_storage_bucket" "terraform-demo-bucket" {
  name          = "terraform-demo-bucket-omole123"
  location      = "US"
  force_destroy = true


  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}