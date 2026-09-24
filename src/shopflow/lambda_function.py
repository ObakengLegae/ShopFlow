import boto3
import urllib.parse
import traceback
import logging
import os
from datetime import datetime

from src.shopflow.pipeline import Pipeline
from src.shopflow.database.database import Database
from src.shopflow.uploader import Uploader

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Lambda triggered by S3 event")

    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
        logger.info(f"Processing Bucket: {bucket}, Key: {key}")

        download_path = f"/tmp/{os.path.basename(key)}"
        logger.info(f"Downloading file to {download_path}")
        s3_client.download_file(bucket, key, download_path)

        lambda_task_root = os.environ.get('LAMBDA_TASK_ROOT', '.')
        schema_path = f"{lambda_task_root}/sql/schema.sql"

        base_name = os.path.basename(key)
        name, ext = os.path.splitext(base_name)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        processed_backup_path = f"/tmp/{name}_processed_{timestamp}{ext}"

        logger.info("Initializing Pipeline with Cloud-Oriented Paths")

        uploader = Uploader(bucket_name=bucket, s3_prefix="processed/")

        cloud_pipeline = Pipeline(
            raw_data_path=download_path,
            processed_data_path=processed_backup_path,
            sql_file_path=schema_path,
            database=Database(),
            uploader=uploader
        )

        logger.info("Triggering cloud pipeline run")
        cloud_pipeline.run()

        logger.info("Pipeline completed successfully inside Lambda.")

        return {
            'statusCode': 200,
            'body': f"File {key} processed by Pipeline successfully!"
        }

    except Exception as e:
        logger.error(f"Error executing pipeline for {key}: {e}")
        logger.error(traceback.format_exc())
        raise e