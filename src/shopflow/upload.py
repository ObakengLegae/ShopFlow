import boto3
import os
import sys
import logging

from botocore.exceptions import NoCredentialsError, ClientError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_file_to_s3(file_path: str, bucket_name: str, object_name: str = None):
    """Uploads a local file to an AWS S3 bucket."""
    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        return False

    if object_name is None:
        object_name = os.path.basename(file_path)

    s3_client = boto3.client('s3')

    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
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

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python upload.py <path_to_file> <s3_bucket_name>")
        sys.exit(1)

    local_file_path = sys.argv[1]
    bucket_name = sys.argv[2]
    upload_file_to_s3(local_file_path, bucket_name)