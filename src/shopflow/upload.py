import boto3
import os
import sys
import logging

from botocore.exceptions import NoCredentialsError, ClientError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Uploader:
    def __init__(self, bucket_name: str = None, s3_prefix: str = "processed/"):
        """
        Initializes the Uploader.
        :param bucket_name: The destination S3 bucket name. If None, uploading is skipped.
        :param s3_prefix: The folder to upload the file to in s3
        """
        self.bucket_name = bucket_name
        self.s3_prefix = s3_prefix

        try:
            self.s3_client = boto3.client('s3')
        except Exception as e:
            logger.warning(f"Failed to initialize S3 client: {e}")
            self.s3_client = None

    def upload(self, file_path: str, object_name: str = None) -> bool:
        """Uploads a local file to an AWS S3 bucket."""
        if not self.bucket_name or self.s3_client:
            logger.info("No bucket name configured or s3 client missing, skipping upload")
            return False

        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        if object_name is None:
            file_name = os.path.basename(file_path)
            object_name = f"{self.s3_prefix}{file_name}"

        try:
            logger.info(f"Uploading {file_path} to s3://{self.bucket_name}/{object_name}")
            self.s3_client.upload_file(file_path, self.bucket_name, object_name)
            logger.info("Uploaded successfully")
            return True

        except FileNotFoundError:
            logger.error(f"File not found")
            return False

        except NoCredentialsError:
            logger.error(f"Credentials not available")
            return False
        except ClientError as e:
            logger.error(e)
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python upload.py <path_to_file> <s3_bucket_name>")
        sys.exit(1)

    local_file_path = sys.argv[1]
    bucket_name = sys.argv[2]

    uploader = Uploader(bucket_name=bucket_name, s3_prefix="")
    uploader.upload_file_to_s3(local_file_path)