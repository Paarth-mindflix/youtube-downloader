import boto3
from loguru import logger
import os
from dotenv import load_dotenv
from pathlib import Path
# Load environment variables from the .env file
env_path = Path(".") / ".env"
load_dotenv()

def upload_file_to_s3(local_file, bucket, s3_key, logger):
    """
    Upload a single file to an S3 bucket.

    :param local_file: Path to the local file.
    :param bucket: Name of the S3 bucket.
    :param s3_key: Path and name of the file in the S3 bucket.
    """
    # Create an S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_SECRET_KEY"),
        region_name='ap-south-1'  # Change to your desired region if needed
    )

    try:
        # Upload the file
        s3_client.upload_file(local_file, bucket, s3_key)
        logger.info(f"Uploaded {local_file} to s3://{bucket}/{s3_key}")
        return True
    except Exception as e:
        logger.info(f"Error uploading file: {e}")
        return False
