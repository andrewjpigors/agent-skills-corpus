---
name: terraform-iac
description: Use when provisioning infrastructure with Terraform, implementing modules, state management, workspace management, remote backends, provider configuration, Sentinel policies, Terratest integration, and production IaC best practices. Covers AWS, Azure, GCP providers and Terraform Cloud/Enterprise integration.
license: MIT
---

# Terraform Infrastructure as Code Skill — IaC Best Practices

## Overview

This skill provides comprehensive guidance for **provisioning and managing infrastructure with Terraform**, including module design, state management, workspace organization, remote backend configuration, provider management, Sentinel policies, Terratest integration, and production-ready Infrastructure as Code practices. Based on HashiCorp official documentation and HashiCorp Certified: Terraform Associate (003) certification standards.

## When to Use

**Use this skill when:**

- Provisioning cloud infrastructure (AWS, Azure, GCP) with Terraform
- Creating reusable Terraform modules with inputs and outputs
- Managing Terraform state with S3/DynamoDB remote backends
- Configuring Terraform workspaces for multi-environment deployments
- Setting up provider configurations with version pinning
- Implementing Terraform Cloud/Enterprise workflows
- Writing Sentinel policies for compliance enforcement
- Integrating Terratest for infrastructure testing
- Importing existing infrastructure into Terraform state
- Detecting and remediating configuration drift
- Managing Terraform state files (mv, rm, list, pull, push)
- Configuring TFLint for static analysis
- Implementing Terraform formatting and validation pipelines
- Designing variable definitions with validation rules
- Using data sources for external data lookups
- Implementing provisioners (shell, file, remote-exec)
- Publishing modules to Terraform Registry
- Managing Terraform outputs and local values
- Using Terraform Console for interactive exploration
- Setting up CI/CD pipelines with Terraform plan/apply
- Destroying infrastructure safely with dependency awareness

**Do NOT use this skill when:**

- Deploying containerized applications (use docker-containerization skill)
- Orchestrating Kubernetes workloads (use kubernetes-orchestration skill)
- Writing application code (use backend-developer or frontend-developer skill)
- Configuring CI/CD pipeline orchestration (use devops-pipeline skill)
- Managing database schema migrations (use database-design skill)
- Implementing serverless functions (use aws-serverless skill)
- Setting up monitoring dashboards (use monitoring skill)
- Writing Pulumi or CloudFormation templates (use cloud-specific IaC skill)

**Why avoid:** Terraform is for infrastructure provisioning and lifecycle management, not application deployment, container orchestration, or continuous integration. Use the right tool for infrastructure definition vs application delivery.

## Core Concepts

### Terraform Workflow Lifecycle

| Phase          | Command              | Purpose                                             |
| -------------- | -------------------- | --------------------------------------------------- |
| **Initialize** | `terraform init`     | Download providers, modules, configure backend      |
| **Validate**   | `terraform validate` | Check configuration syntax and internal consistency |
| **Format**     | `terraform fmt`      | Auto-format HCL code for consistency                |
| **Plan**       | `terraform plan`     | Preview changes without applying                    |
| **Apply**      | `terraform apply`    | Create/update/delete resources                      |
| **Destroy**    | `terraform destroy`  | Remove all managed resources                        |
| **Import**     | `terraform import`   | Add existing resources to state                     |
| **Console**    | `terraform console`  | Interactive expression evaluation                   |

### State Management Strategies

| Strategy            | Use Case                                 | Backend                          |
| ------------------- | ---------------------------------------- | -------------------------------- |
| **Local State**     | Personal projects, experimentation       | `terraform.tfstate` (local file) |
| **Remote S3**       | Team collaboration, production           | AWS S3 + DynamoDB locking        |
| **Terraform Cloud** | Enterprise workflows, team collaboration | HashiCorp-managed backend        |
| **Azure RM**        | Azure-native deployments                 | Azure Blob Storage               |
| **GCS**             | GCP-native deployments                   | Google Cloud Storage             |

### Module Design Patterns

| Pattern            | Description                   | When to Use                            |
| ------------------ | ----------------------------- | -------------------------------------- |
| **Root Module**    | Top-level configuration       | Entry point for `terraform apply`      |
| **Child Module**   | Reusable component            | Network, compute, storage abstractions |
| **Nested Module**  | Module calling another module | Complex compositions                   |
| **Wrapper Module** | Registry module with defaults | Customizing community modules          |
| **Factory Module** | Dynamic resource creation     | Count/for_each driven resources        |

## Provider Configuration

### Multi-Provider Setup

```hcl
# ============================================
# Provider Configuration with Version Pinning
# ============================================

terraform {
  required_version = ">= 1.5.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

# AWS Provider
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Environment = var.environment
      ManagedBy   = "terraform"
      Project     = var.project_name
    }
  }
}

# AWS Provider for secondary region
provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

# Azure Provider
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
    key_vault {
      purge_soft_delete_on_destroy = true
    }
  }
}

# GCP Provider
provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}
```

### Provider Aliases for Multi-Region

```hcl
# Use aliased provider
resource "aws_instance" "west_us" {
  provider = aws.west

  ami           = data.aws_ami.amazon_linux.id
  instance_type = "t3.micro"

  tags = {
    Name    = "west-us-instance"
    Region  = "us-west-2"
  }
}
```

## Backend Configuration

### S3 + DynamoDB (Recommended for AWS)

```hcl
terraform {
  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "production/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true

    skip_metadata_api_check     = false
    skip_region_validation      = false
    skip_credentials_validation = false
  }
}
```

### Terraform Cloud Backend

```hcl
terraform {
  cloud {
    organization = "my-organization"

    workspaces {
      name = "production-infrastructure"
    }
  }
}
```

### Azure Backend

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "terraformstatestor"
    container_name       = "tfstate"
    key                  = "production.tfstate"
  }
}
```

## Module Design

### Well-Structured Module

```hcl
# ============================================
# Module: VPC with Public and Private Subnets
# ============================================

variable "vpc_cidr" {
  type        = string
  description = "CIDR block for the VPC"
  default     = "10.0.0.0/16"

  validation {
    condition     = can(cidrhost(var.vpc_cidr, 0))
    error_message = "Must be a valid CIDR block."
  }
}

variable "environment" {
  type        = string
  description = "Deployment environment name"

  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be development, staging, or production."
  }
}

variable "public_subnet_count" {
  type        = number
  description = "Number of public subnets to create"
  default     = 3

  validation {
    condition     = var.public_subnet_count >= 1 && var.public_subnet_count <= 10
    error_message = "Must be between 1 and 10."
  }
}

# Local values for computed configurations
locals {
  name_prefix = "${var.project_name}-${var.environment}"

  availability_zones = data.aws_availability_zones.available.names

  public_subnet_cidrs = [
    for i in range(var.public_subnet_count) :
    cidrsubnet(var.vpc_cidr, 8, i)
  ]

  private_subnet_cidrs = [
    for i in range(var.public_subnet_count) :
    cidrsubnet(var.vpc_cidr, 8, i + var.public_subnet_count)
  ]
}

# Data source
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC Resource
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}

# Public Subnets with for_each
resource "aws_subnet" "public" {
  for_each = toset(local.public_subnet_cidrs)

  vpc_id                  = aws_vpc.main.id
  cidr_block              = each.value
  availability_zone       = local.availability_zones[index(local.public_subnet_cidrs, each.value)]
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.name_prefix}-public-${index(local.public_subnet_cidrs, each.value)}"
    Tier = "public"
  }
}

# Private Subnets with count
resource "aws_subnet" "private" {
  count             = var.public_subnet_count
  vpc_id            = aws_vpc.main.id
  cidr_block        = local.private_subnet_cidrs[count.index]
  availability_zone = local.availability_zones[count.index]

  tags = {
    Name = "${local.name_prefix}-private-${count.index}"
    Tier = "private"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.name_prefix}-igw"
  }
}

# Outputs
output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = [for s in aws_subnet.public : s.id]
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}
```

### Using a Module

```hcl
module "vpc" {
  source = "./modules/vpc"

  project_name        = "myapp"
  environment         = "production"
  vpc_cidr            = "10.0.0.0/16"
  public_subnet_count = 3
}

# Access module outputs
output "vpc_id" {
  value = module.vpc.vpc_id
}
```

## Variables and Outputs

### Variable Definitions with Validation

```hcl
variable "instance_type" {
  type        = string
  description = "EC2 instance type"
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Instance type must be t2 or t3 family."
  }
}

variable "allowed_security_group_ids" {
  type        = list(string)
  description = "List of security group IDs to attach"
  default     = []
}

variable "extra_tags" {
  type        = map(string)
  description = "Additional tags to apply"
  default     = {}
}

variable "database_config" {
  type = object({
    engine         = string
    engine_version = string
    instance_class = string
    allocated_storage = number
  })
  description = "RDS database configuration"

  default = {
    engine         = "postgres"
    engine_version = "15.4"
    instance_class = "db.t3.medium"
    allocated_storage = 100
  }
}
```

### Sensitive Variables

```hcl
variable "database_password" {
  type        = string
  description = "Master password for the database"
  sensitive   = true

  # Never use default for sensitive values
  # Pass via environment variable: TF_VAR_database_password
}

variable "api_keys" {
  type = map(string)
  description = "API keys for external services"
  sensitive = true
}
```

### Output Definitions

```hcl
output "database_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.main.endpoint
  sensitive   = false
}

output "database_credentials" {
  description = "Database connection credentials"
  value = {
    username = var.database_username
    password = var.database_password
    endpoint = aws_db_instance.main.endpoint
  }
  sensitive = true
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id

  # Prevent accidental exposure in dependent modules
  sensitive = false
}
```

## Workspaces

### Workspace Management

```bash
# List workspaces
terraform workspace list

# Create workspace
terraform workspace new staging

# Select workspace
terraform workspace select production

# Delete workspace (must be empty)
terraform workspace delete staging

# Show current workspace
terraform workspace show
```

### Workspace-Aware Configuration

```hcl
terraform {
  backend "s3" {
    bucket         = "myapp-terraform-state"
    key            = "infrastructure/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-state-lock"
    encrypt        = true
  }
}

# Use workspace name in resource configuration
locals {
  environment = terraform.workspace

  # Fallback for default workspace
  env_suffix = terraform.workspace != "default" ? terraform.workspace : "dev"

  name_prefix = "${var.project_name}-${local.env_suffix}"
}

resource "aws_s3_bucket" "data" {
  bucket = "${local.name_prefix}-data-bucket"

  tags = {
    Environment = local.environment
    Name        = "${local.name_prefix}-data"
  }
}
```

## State Management

### State Commands

```bash
# List resources in state
terraform state list

# Show resource details
terraform state show aws_instance.example

# Move resource within state
terraform state mv aws_instance.old aws_instance.new

# Move resource between modules
terraform state mv module.a.aws_instance.example module.b.aws_instance.example

# Remove resource from state (without destroying)
terraform state rm aws_instance.example

# Pull state to stdout
terraform state pull

# Push state from local to remote
terraform state push terraform.tfstate

# Replace provider in state (after provider upgrade)
terraform state replace-provider hashicorp/aws registry.terraform.io/hashicorp/aws
```

### State Locking

```hcl
# DynamoDB table for state locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-state-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name = "Terraform State Lock"
  }
}
```

## Data Sources

### Common Data Source Patterns

```hcl
# AMI Lookup
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

# Current AWS Info
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}
data "aws_availability_zones" "available" {
  state = "available"
}

# VPC Lookup
data "aws_vpc" "existing" {
  id = var.existing_vpc_id
}

# Security Group Lookup
data "aws_security_group" "existing" {
  id = var.existing_sg_id
}

# External Data Source
data "external" "ip_ranges" {
  program = ["bash", "${path.module}/scripts/get_ip_ranges.sh"]

  query = {
    environment = var.environment
  }
}
```

## Provisioners

### Connection and Provisioner Patterns

```hcl
resource "aws_instance" "app" {
  ami           = data.aws_ami.amazon_linux.id
  instance_type = var.instance_type

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              EOF

  # File provisioner
  provisioner "file" {
    source      = "config/"
    destination = "/tmp/config/"

    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file(var.private_key_path)
      timeout     = "2m"
    }
  }

  # Remote-exec provisioner
  provisioner "remote-exec" {
    inline = [
      "sudo cp /tmp/config/* /etc/app/",
      "sudo systemctl restart app",
    ]

    connection {
      type        = "ssh"
      host        = self.public_ip
      user        = "ec2-user"
      private_key = file(var.private_key_path)
    }
  }

  # Local-exec provisioner
  provisioner "local-exec" {
    command = "echo ${self.public_ip} > instance_ip.txt"
  }

  tags = {
    Name = "app-server"
  }
}
```

### Provisioner Best Practices

```hcl
# GOOD: Use user_data for bootstrapping
user_data = <<-EOF
            #!/bin/bash
            # Install and configure application
            EOF

# GOOD: Use provisioner "local-exec" for side effects
provisioner "local-exec" {
  command = "echo ${aws_db_instance.main.endpoint} > db_endpoint.txt"
}

# BAD: Avoid remote-exec for complex configurations
# Use Cloud-Init, Ansible, Packer, or configuration management instead
provisioner "remote-exec" {
  # Complex multi-line scripts are hard to debug
  inline = [
    "very complex script that is difficult to maintain",
  ]
}

# GOOD: Use provisioner "local-exec" with when condition
provisioner "local-exec" {
  when    = destroy
  command = "rm -f instance_ip.txt"
}
```

## Import Existing Infrastructure

### Import Workflow

```bash
# 1. Write the resource configuration
# 2. Run import command
terraform import aws_instance.existing i-0abc123def456789

# 3. Verify state
terraform state show aws_instance.existing

# 4. Run plan to confirm no changes
terraform plan

# Import module resources
terraform import module.vpc.aws_subnet.public[0] subnet-0abc123def456789

# Import with state push (for remote backend)
terraform state pull > local.tfstate
terraform import aws_instance.example i-0abc123def456789
terraform state push local.tfstate
```

### Import with Generated Configuration (Terraform 1.0+)

```bash
# Generate configuration from existing resource
terraform import -generate-config=imported.tf aws_instance.existing i-0abc123def456789

# Review generated configuration in imported.tf
# Adjust as needed and merge into your configuration
```

## Drift Detection

### Detecting and Remediating Drift

```bash
# Detect drift
terraform plan -detect-drift

# Show only drift (no planned changes)
terraform plan -refresh-only

# Force refresh state
terraform apply -refresh-only

# Detect drift in CI/CD
terraform plan -no-color -detailed-exitcode
# Exit code 0: no changes
# Exit code 1: error
# Exit code 2: changes detected (including drift)
```

## Terraform Cloud/Enterprise

### Remote Operations

```bash
# Login to Terraform Cloud
terraform login

# Run plan remotely
terraform plan -input=false

# Run apply remotely
terraform apply -auto-approve

# Run with specific workspace
terraform workspace select production
```

### Terraform Cloud Configuration

```hcl
terraform {
  cloud {
    organization = "my-organization"

    workspaces {
      name = "production-infrastructure"
      tags = ["production", "infrastructure"]
    }
  }
}

# Variables are managed in Terraform Cloud UI
# State is stored in Terraform Cloud
# Run tasks and Sentinel policies are enforced
```

## Sentinel Policies

### Policy Examples

```hcl
# ============================================
# Sentinel Policy: Enforce Tagging
# ============================================

import "tfplan"

# Require all resources to have Environment tag
required_tags = {"Environment", "Project", "ManagedBy"}

violations = []

for tfplan.resource_changes as address, rc {
  if rc.mode is "managed" {
    for required_tags as tag {
      if rc.change.after.tags is null or rc.change.after.tags[tag] is null {
        violations += [address + " missing required tag: " + tag]
      }
    }
  }
}

main = rule {
  length(violations) == 0 else violations
}
```

### Cost Estimation Policy

```hcl
import "tfplan"
import "findings"

# Prevent resources that exceed cost threshold
expensive_resources = findings.expensive_resources(
  tfplan.resource_changes,
  1000  # $1000/month threshold
)

main = rule {
  length(expensive_resources) == 0 else expensive_resources
}
```

## Terratest Integration

### Infrastructure Testing

```go
// terraform/vpc_test.go
package test

import (
    "testing"
    "github.com/gruntwork-io/terratest/modules/terraform"
    "github.com/gruntwork-io/terratest/modules/aws"
    "github.com/stretchr/testify/assert"
)

func TestTerraformVPCModule(t *testing.T) {
    t.Parallel()

    terraformOptions := &terraform.Options{
        TerraformDir: "../modules/vpc",
        Variables: map[string]interface{}{
            "project_name":        "test",
            "environment":         "testing",
            "vpc_cidr":            "10.0.0.0/16",
            "public_subnet_count": 3,
        },
        EnvVars: map[string]string{
            "AWS_ACCESS_KEY_ID":     "test-key",
            "AWS_SECRET_ACCESS_KEY": "test-secret",
            "AWS_DEFAULT_REGION":    "us-east-1",
        },
    }

    defer terraform.Cleanup(t, terraformOptions)

    // Run terraform apply
    terraform.InitAndApply(t, terraformOptions)

    // Get outputs
    vpcCidr := terraform.Output(t, terraformOptions, "vpc_cidr")
    publicSubnetIds := terraform.OutputList(t, terraformOptions, "public_subnet_ids")

    // Verify VPC
    assert.Equal(t, "10.0.0.0/16", vpcCidr)
    assert.Equal(t, 3, len(publicSubnetIds))

    // Verify VPC exists in AWS
    vpc := aws.GetVpcById(t, publicSubnetIds[0], "us-east-1")
    assert.Equal(t, "10.0.0.0/16", *vpc.CidrBlock)
}
```

## TFLint Configuration

### .tflint.hcl

```hcl
plugin "aws" {
    enabled = true
    version = "0.32.0"
    source  = "github.com/terraform-linters/tflint-ruleset-aws"
}

config {
    caller_references    = true
    force                = false
    hide_warning_on_run  = false
    var_file             = ["terraform.tfvars"]
}

rule "terraform_deprecated_index" {
    enabled = true
}

rule "terraform_documented_outputs" {
    enabled = true
}

rule "terraform_documented_variables" {
    enabled = true
}

rule "terraform_typed_variables" {
    enabled = true
}

rule "terraform_naming_convention" {
    enabled = true
    format = "snake_case"
}

rule "terraform_required_version" {
    enabled = true
}

rule "terraform_required_provider" {
    enabled = true
}

rule "aws_instance_type_not_upgradeable" {
    enabled = true
}

rule "aws_resource_missing_tags" {
    enabled = true
    allowed_tags = ["Environment", "Project", "ManagedBy"]
}
```

### Running TFLint

```bash
# Install TFLint
# macOS: brew install tflint
# Linux: curl -s https://raw.githubusercontent.com/terraform-linters/tflint/master/install.sh | bash

# Initialize plugins
tflint --init

# Run TFLint
tflint

# Run with specific var file
tflint --var-file=terraform.tfvars

# Run in CI (exit on warning)
tflint --force
```

## Formatting and Validation

### Automated Formatting

```bash
# Format all files
terraform fmt

# Format recursively
terraform fmt -recursive

# Check formatting without modifying
terraform fmt -check -recursive

# Write diff of formatting changes
terraform fmt -diff -recursive > fmt.diff
```

### Validation Pipeline

```bash
# Complete validation pipeline
terraform fmt -check -recursive && \
terraform validate && \
tflint --force && \
terraform plan -no-color

# Exit codes:
# 0 = success
# 1 = validation/formatting failed
# 2 = changes detected in plan
```

## Production Best Practices

### Project Structure

```
infrastructure/
├── modules/
│   ├── vpc/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   └── README.md
│   ├── ecs/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── rds/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/
│   ├── development/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf
│   └── production/
│       ├── main.tf
│       ├── variables.tf
│       ├── terraform.tfvars
│       └── backend.tf
├── scripts/
│   ├── validate.sh
│   └── get_ip_ranges.sh
├── .tflint.hcl
├── .terraform.lock.hcl
└── README.md
```

### CI/CD Pipeline Integration

```yaml
# GitHub Actions Example
name: Terraform CI/CD
on:
  pull_request:
    paths:
      - 'infrastructure/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: hashicorp/setup-terraform@v3
        with:
          terraform_version: '1.5.0'

      - name: Terraform Format Check
        run: terraform fmt -check -recursive

      - name: Terraform Init
        run: terraform init
        working-directory: infrastructure/environments/production

      - name: Terraform Validate
        run: terraform validate
        working-directory: infrastructure/environments/production

      - name: TFLint
        uses: terraform-linters/setup-tflint@v4
        with:
          tflint_version: v0.50.0

      - name: TFLint Init
        run: tflint --init
        working-directory: infrastructure

      - name: TFLint Run
        run: tflint --force
        working-directory: infrastructure

      - name: Terraform Plan
        run: terraform plan -no-color -input=false
        working-directory: infrastructure/environments/production
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1
```

### Security Best Practices

```hcl
# GOOD: Version pin providers
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# GOOD: Mark sensitive variables
variable "database_password" {
  type      = string
  sensitive = true
}

# GOOD: Use data sources over hardcoded values
data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]
}

# GOOD: Enable state encryption
terraform {
  backend "s3" {
    bucket  = "terraform-state"
    key     = "prod/terraform.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

# GOOD: Use .terraform.lock.hcl (commit to version control)
# Prevents provider version drift

# BAD: Hardcode secrets
resource "aws_db_instance" "bad" {
  password = "mysecretpassword123"  # Never do this!
}

# BAD: Use latest provider versions
required_providers {
  aws = {
    source  = "hashicorp/aws"
    version = "~> 5.0"  # Good: pinned range
    # version = ">= 5.0"  # Bad: no upper bound
  }
}

# BAD: Disable state locking
# Always use DynamoDB or Terraform Cloud for state locking
```

## Anti-Patterns

### Common Mistakes

```hcl
# BAD: Using count for everything
resource "aws_security_group_rule" "bad" {
  count = length(var.inbound_rules)
  # Hard to add/remove individual rules
}

# GOOD: Using for_each when possible
resource "aws_security_group_rule" "good" {
  for_each = { for rule in var.inbound_rules : rule.cidr => rule }

  type        = "ingress"
  from_port   = each.value.from_port
  to_port     = each.value.to_port
  protocol    = each.value.protocol
  cidr_blocks = [each.value.cidr]
}

# BAD: Creating resources without lifecycle rules
resource "aws_s3_bucket" "bad" {
  bucket = "my-bucket"
  # Will be destroyed on rename
}

# GOOD: Using lifecycle rules
resource "aws_s3_bucket" "good" {
  bucket = "my-bucket"

  lifecycle {
    prevent_destroy         = false    # Set true for critical resources
    create_before_destroy   = true     # For unique name resources
    ignore_changes          = [tags]   # Ignore tag changes from external tools
  }
}

# BAD: Ignoring state file
# terraform.tfstate should NOT be committed to version control
# Use remote backend instead

# BAD: Using hardcoded IDs
resource "aws_instance" "bad" {
  ami = "ami-0abc123def4567890"  # Region-specific, will break
}

# GOOD: Using data sources
resource "aws_instance" "good" {
  ami = data.aws_ami.amazon_linux.id  # Dynamic lookup
}
```

## Production Checklist

Before deploying to production:

- [ ] Provider versions pinned with upper bounds
- [ ] Remote backend configured with state locking
- [ ] State encryption enabled
- [ ] Sensitive variables marked as `sensitive = true`
- [ ] All variables have descriptions
- [ ] All outputs have descriptions
- [ ] Modules follow single-responsibility principle
- [ ] `.terraform.lock.hcl` committed to version control
- [ ] `terraform fmt -recursive` passes
- [ ] `terraform validate` passes
- [ ] TFLint configured and passes
- [ ] Sentinel policies defined for compliance
- [ ] Terratest tests written for critical modules
- [ ] CI/CD pipeline validates before apply
- [ ] Workspace strategy defined for environments
- [ ] State file access restricted (IAM policies)
- [ ] Drift detection scheduled
- [ ] Rollback procedure documented
- [ ] Tags applied to all resources
- [ ] No hardcoded secrets in configuration
- [ ] User data scripts idempotent
- [ ] Lifecycle rules defined for critical resources

## Real-World Impact

**Before this skill:**

- Manual cloud console clicks for infrastructure
- No version control for infrastructure changes
- State file conflicts between team members
- No validation before applying changes
- Hardcoded secrets in configuration
- No testing for infrastructure code
- Configuration drift goes undetected

**After this skill:**

- Infrastructure defined as version-controlled code
- Automated validation and linting in CI/CD
- Remote state with locking for team collaboration
- Sentinel policies enforce compliance
- Terratest validates infrastructure behavior
- Drift detection alerts on manual changes
- Reproducible environments across teams

## Cross-References

- **`docker-containerization`** - For building container images deployed to infrastructure
- **`kubernetes-orchestration`** - For deploying to Terraform-provisioned EKS/AKS/GKE clusters
- **`devops-pipeline`** - For CI/CD integration with Terraform workflows
- **`aws-serverless`** - For AWS-specific serverless infrastructure
- **`security-auditor`** - For security review of Terraform configurations
- **`disaster-recovery`** - For multi-region disaster recovery infrastructure

## References

- [Terraform Documentation](https://developer.hashicorp.com/terraform/docs)
- [Terraform Language Reference](https://developer.hashicorp.com/terraform/language)
- [Terraform Registry](https://registry.terraform.io/)
- [Terraform Cloud Documentation](https://developer.hashicorp.com/terraform/cloud-docs)
- [Terraform Associate (003) Study Guide](https://www.hashicorp.com/certification/terraform-associate)
- [Terraform Best Practices](https://www.terraform-best-practices.com/)
- [Sentinel Documentation](https://developer.hashicorp.com/sentinel/docs)
- [Terratest Documentation](https://terratest.gruntwork.io/)
- [TFLint Documentation](https://github.com/terraform-linters/tflint)
- [AWS Provider Documentation](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Google Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
