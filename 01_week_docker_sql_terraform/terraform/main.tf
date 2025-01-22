terraform {
  required_providers {
    google = {
        source = "hashicorp/google"
        version = "6.16.0"
    }
  }
}

provider "google" {
    credentials = file(var.credentials)
    project = var.project
    region = var.region
}

resource "google_storage_bucket" "ramiz_de_zoomcamp_bucket" {
    name = var.gcs_bucket_name
    location = var.location
    force_destroy = true
}

resource "google_bigquery_dataset" "ramiz_de_zoompcamp_dataset" {
    dataset_id = var.bq_dataset_name
    location = var.location
}