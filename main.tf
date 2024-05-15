terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 4.34.0"
    }
  }
}

provider "google" {
  project = var.project
  region  = var.region
}

variable "services" {
  type = list(string)
  default = [
    "run.googleapis.com",
    "cloudfunctions.googleapis.com",
    "iam.googleapis.com",
    "cloudbuild.googleapis.com",
  ]
}

resource "google_project_service" "services" {
  for_each = toset(var.services)
  project  = var.project
  service  = each.value
}

resource "random_id" "default" {
  byte_length = 8
}

resource "google_storage_bucket" "default" {
  name                        = "${random_id.default.hex}-gcf-source" # Every bucket name must be globally unique
  location                    = var.region
  uniform_bucket_level_access = true
}

data "archive_file" "default" {
  type        = "zip"
  output_path = "/tmp/function-source.zip"
  source_dir  = "src/"
}


locals {
  source_code_hash = filemd5(data.archive_file.default.output_path)
  config           = yamldecode(file("${path.module}/prod.env.yaml"))
}

resource "google_service_account" "service_account" {
  account_id   = "${var.name}-sa"
  display_name = "Service Account"
}

resource "google_storage_bucket_object" "object" {
  name   = "function-source-${local.source_code_hash}.zip"
  bucket = google_storage_bucket.default.name
  source = data.archive_file.default.output_path # Add path to the zipped function source code
}

resource "google_cloudfunctions2_function" "bot" {
  depends_on = [
    google_storage_bucket_object.object,
    google_service_account.service_account,
    google_project_service.services,

  ]
  name        = var.name
  description = var.description

  location = var.region

  build_config {
    runtime     = "python312"
    entry_point = "handle" # Set the entry point
    source {
      storage_source {
        bucket = google_storage_bucket.default.name
        object = google_storage_bucket_object.object.name
      }
    }

  }

  service_config {
    max_instance_count    = 1
    available_memory      = "256M"
    timeout_seconds       = 60
    ingress_settings      = "ALLOW_ALL"
    environment_variables = local.config
    service_account_email = google_service_account.service_account.email
  }
}


resource "google_cloudfunctions2_function_iam_member" "v2invoker" {
  depends_on = [google_cloudfunctions2_function.bot]

  project        = google_cloudfunctions2_function.bot.project
  cloud_function = google_cloudfunctions2_function.bot.name
  location       = google_cloudfunctions2_function.bot.location

  role   = "roles/cloudfunctions.invoker"
  member = "allUsers"
}

resource "google_cloudfunctions2_function_iam_binding" "binding" {
  depends_on = [google_cloudfunctions2_function.bot]

  project        = google_cloudfunctions2_function.bot.project
  location       = google_cloudfunctions2_function.bot.location
  cloud_function = google_cloudfunctions2_function.bot.name
  role           = "roles/cloudfunctions.invoker"
  members        = ["allUsers"]
}


