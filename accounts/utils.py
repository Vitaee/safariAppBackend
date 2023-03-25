from botocore.exceptions import ClientError
from django.conf import settings
import boto3

s3 = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION_NAME
)

def upload_file_to_s3(file_obj, file_name):
    try:
        s3.upload_fileobj(file_obj, settings.AWS_S3_BUCKET_NAME, file_name)
        url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION_NAME}.amazonaws.com/{file_name}"
        return url
    except ClientError as e:
        print(e)
        return None