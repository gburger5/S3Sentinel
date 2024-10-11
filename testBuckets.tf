# Set the AWS provider to use us-east-1 region
provider "aws" {
  region = "us-east-1"
}

# 1. Bucket with no encryption
resource "aws_s3_bucket" "no_encryption" {
  bucket = "unique-gabeb5-test-no-encryption-bucket"
}

# 2. Bucket with encryption
resource "aws_s3_bucket" "with_encryption" {
  bucket = "unique-gabeb5-test-with-encryption-bucket"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "with_encryption" {
  bucket = aws_s3_bucket.with_encryption.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# 3. Bucket with versioning enabled
resource "aws_s3_bucket" "with_versioning" {
  bucket = "unique-gabeb5-test-with-versioning-bucket"
}

resource "aws_s3_bucket_versioning" "with_versioning" {
  bucket = aws_s3_bucket.with_versioning.id
  versioning_configuration {
    status = "Enabled"
  }
}

# 4. Bucket with public access block disabled
resource "aws_s3_bucket" "public_access_enabled" {
  bucket = "unique-gabeb5-test-public-access-enabled-bucket"
}

resource "aws_s3_bucket_public_access_block" "public_access_enabled" {
  bucket = aws_s3_bucket.public_access_enabled.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# 5. Bucket with logging enabled
resource "aws_s3_bucket" "with_logging" {
  bucket = "unique-gabeb5-test-with-logging-bucket"
}

resource "aws_s3_bucket" "log_bucket" {
  bucket = "unique-gabeb5-test-log-bucket"
}

resource "aws_s3_bucket_logging" "with_logging" {
  bucket = aws_s3_bucket.with_logging.id

  target_bucket = aws_s3_bucket.log_bucket.id
  target_prefix = "log/"
}

# 6. Bucket with lifecycle rule
resource "aws_s3_bucket" "with_lifecycle" {
  bucket = "unique-gabeb5-test-with-lifecycle-bucket"
}

resource "aws_s3_bucket_lifecycle_configuration" "with_lifecycle" {
  bucket = aws_s3_bucket.with_lifecycle.id

  rule {
    id     = "rule-1"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 90
    }
  }
}

# 7. Bucket with concerning ACL (public read access)
resource "aws_s3_bucket" "public_read" {
  bucket = "unique-gabeb5-test-public-read-bucket"
}

resource "aws_s3_bucket_public_access_block" "public_read" {
  bucket = aws_s3_bucket.public_read.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}


# Output the bucket names for reference
output "bucket_names" {
  value = [
    aws_s3_bucket.no_encryption.id,
    aws_s3_bucket.with_encryption.id,
    aws_s3_bucket.with_versioning.id,
    aws_s3_bucket.public_access_enabled.id,
    aws_s3_bucket.with_logging.id,
    aws_s3_bucket.with_lifecycle.id,
    aws_s3_bucket.public_read.id
  ]
}