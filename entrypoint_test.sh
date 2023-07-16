#!/bin/sh


python manage.py collectstatic --noinput --clear --settings=safariBackend.settings.test 
python manage.py makemigrations --settings=safariBackend.settings.test
python manage.py migrate --settings=safariBackend.settings.test 
python manage.py runserver --settings=safariBackend.settings.test 0.0.0.0:6000 
celery -A safariBackend worker --loglevel=info 
celery -A safariBackend beat -l debug

echo "$@"
exec "$@"