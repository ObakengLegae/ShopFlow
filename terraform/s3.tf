resource "aws_s3_bucket" "data_storage" {
    bucket_prefix = "shopflow-data"

    tags = {
        Project     = "Shopflow"
        Environment = "dev"
    }
}

resource "aws_s3_bucket_public_access_block" "data_storage_access" {
    bucket = aws_s3_bucket.data_storage.id

    block_public_acls       = true
    block_public_policy     = true
    ignore_public_acls      = true
    restrict_public_buckets = true
}

output "s3_bucket_name" {
    description = "The name of the s3 bucket."
    value       = aws_s3_bucket.data_storage.bucket
}