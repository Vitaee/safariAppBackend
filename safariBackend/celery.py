import os,json
from celery import Celery
from kombu.serialization import register
from .serializers import BytesJSONEncoder, BytesJSONDecoder
from kombu.utils.json import loads, dumps
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'safariBackend.settings.test')

register(
    'json_bytes',
    lambda v: json.dumps(v, cls=BytesJSONEncoder),
    lambda v: json.loads(v, cls=BytesJSONDecoder),
    content_type='application/json',
    content_encoding='utf-8'
)

app = Celery('safariBackend')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.task_serializer = 'json_bytes'
app.conf.accept_content = ['json_bytes']
app.conf.result_serializer = 'json_bytes'

app.conf.task_serializers = {
    'json' : dumps,
    'json_bytes': 'json_bytes'
}
app.conf.result_serializers = {
    'json': loads,
    'json_bytes': 'json_bytes'
}

app.conf.beat_schedule = {
    'sent-get-request-every-midnight': {
        'task': 'scraper.tasks.cron_scraper',
        'schedule': crontab(minute=0, hour=0),
    },
}