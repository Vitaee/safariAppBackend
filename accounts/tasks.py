from celery import shared_task
from .utils import upload_file_to_s3
from .models import User

@shared_task
def upload_to_s3_task(file_obj, file_name, user_id):
    url = upload_file_to_s3(file_obj, file_name)
    if url:
        user = User.objects.get(pk=user_id)
        user.profile_image = url
        user.save()