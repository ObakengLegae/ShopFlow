data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "${path.module}/.."
    output_path = "${path.module}/lambda.zip"
    excludes    = [".git", "venv", ".idea", "terraform", "data", "__pycache__", ".pytest_cache"]
}

resource "aws_lambda_function" "data_pipeline" {
    filename      = data.archive_file.lambda_zip.output_path
    function_name = "shopflow-s3-to-rds-pipeline"
    role          = aws_iam_role.lambda_exec_role.arn
    handler       = "src.shopflow.lambda_function.lambda_handler"
    runtime       = "python3.11"

    source_code_hash = data.archive_file.lambda_zip.output_base64sha256

    vpc_config {
        subnet_ids         = data.aws_subnets.default.ids
        security_group_ids = [aws_security_group.rds_sg.id]
    }

    environment {
        variables = {
            DB_HOST     = split(":", aws_db_instance.postgres.endpoint)[0]
            DB_USER     = var.db_username
            DB_PASSWORD = var.db_password
            DB_NAME     = "shopflow"
            DB_PORT     = "5432"
        }
    }

    layers = [
        "arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:9"
    ]

    timeout     = 300
    memory_size = 512
}

resource "aws_lambda_permission" "allow_s3_bucket" {
    statement_id  = "AllowExecutionFromS3Bucket"
    action        = "lambda:InvokeFunction"
    function_name = aws_lambda_function.data_pipeline.arn
    principal     = "s3.amazonaws.com"
    source_arn    = aws_s3_bucket.data_storage.arn
}

resource "aws_s3_bucket_notification" "bucket_notification" {
    bucket = aws_s3_bucket.data_storage.id

    lambda_function {
        lambda_function_arn = aws_lambda_function.data_pipeline.arn
        events              = ["s3:ObjectCreated:*"]
        filter_suffix       = ".csv"
    }

    depends_on = [aws_lambda_permission.allow_s3_bucket]
}