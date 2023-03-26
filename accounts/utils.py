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
        content_type = file_obj['content_type']
        file_content = file_obj['chunks']

        # Upload the file to AWS S3
        s3.put_object(
            Bucket=settings.AWS_S3_BUCKET_NAME,
            Key='safariApp/' + file_name,
            Body=b''.join(file_content),
            ContentType=content_type,
        )
        url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.{settings.AWS_REGION_NAME}.amazonaws.com/safariApp/{file_name}"
        return url
    except ClientError as e:
        print(e)
        return None