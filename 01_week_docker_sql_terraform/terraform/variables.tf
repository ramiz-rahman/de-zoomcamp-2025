variable "credentials" {
    description = "Path to JSON Key storing GCP credentials"
    default = "./terrademo_key.json"
}

variable "project" {
    description = "Project ID"
    default = "quick-sonar-447811-r4"
}

variable "region" {
    description = "Region of GCP Server"
    default = "us-central"
}

variable "location" {
    description = "Project Location"
    default = "US"
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default = "ramiz_de_zoomcamp_dataset"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    default = "ramiz_de_zoomcamp_bucket"
}

variable "gcs_storage_class" {
    description = "Bucket Storage Class"
    default = "STANDARD"
}
