# Terraform and GCP Setup

This repository contains Terraform configurations for setting up infrastructure on Google Cloud Platform (GCP).

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed
- A GCP account
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured

## Setup Instructions

1. **Authenticate with GCP:**
    ```sh
    gcloud auth login
    gcloud auth application-default login
    ```

2. **Initialize Terraform:**
    ```sh
    terraform init
    ```

3. **Review and modify the `variables.tf` file to match the requirements.**

4. **Apply the Terraform configuration:**
    ```sh
    terraform apply
    ```

## Project Structure

- `main.tf`: Main Terraform configuration file.
- `variables.tf`: Variable definitions.
- `outputs.tf`: Output definitions.
- `provider.tf`: Provider configuration.

## Resources Created

- VPC
- Subnets
- Compute Instances
- Firewalls

## Cleanup

To destroy the infrastructure created by Terraform, run:
```sh
terraform destroy
```


