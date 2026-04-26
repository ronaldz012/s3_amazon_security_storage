import boto3
from config import settings

_s3_client = None

def init_s3_client():
    global _s3_client
    _s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY,
        aws_secret_access_key=settings.AWS_SECRET_KEY,
        region_name=settings.REGION_NAME,
    )

def get_s3_client():
    if _s3_client is None:
        raise RuntimeError("S3 client no inicializado")
    return _s3_client

def close_s3_client():
    global _s3_client
    _s3_client = None