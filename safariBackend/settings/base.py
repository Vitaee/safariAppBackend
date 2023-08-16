import os
from datetime import timedelta
from pathlib import Path
from decouple import Config, RepositoryEnv
from django.core.management.utils import get_random_secret_key
from django.conf import settings


# generating and printing the SECRET_KEY
BASE_DIR = Path(__file__).resolve().parent.parent.parent


settings_module_name = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[-1]

DOTENV_FILE = f'{BASE_DIR}/.env.{settings_module_name}'

config = Config(RepositoryEnv(DOTENV_FILE))
SCRAPER_BASE_URL=config.get("SCRAPER_URL")
CSRF_TRUSTED_ORIGINS = config.get("CSRF_TRUSTED_ORIGINS").split(" ")

try:
    SECRET_KEY = config.get('SECRET_KEY')
except Exception as e:
    print(e)
    SECRET_KEY = None
    raise "Secret Key is missing in your env fie!"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'accounts.apps.AccountsConfig',
    'safari.apps.SafariConfig',
    'scraper.apps.ScraperConfig',

    'rest_framework',
    'django_cleanup',
    'django_redis',
    'django_elasticsearch_dsl',
    'drf_yasg',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'safariBackend.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'safariBackend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',

    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (

        'rest_framework_simplejwt.authentication.JWTAuthentication',

    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,

}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {filename} {funcName} {lineno} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{asctime} {levelname} - {message}',
            'style': '{',
        },
    },    
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG', # change to DEBUG for more verbose output
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config.get('LOCATION_CACHE_URL'),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "mycache_",
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': "http://elastic:9200",
    },
}



LOCALE_PATHS = os.path.join(BASE_DIR, 'locale/'),
AWS_ACCESS_KEY_ID = config.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config.get('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = config.get('AWS_REGION_NAME')
AWS_S3_BUCKET_NAME = config.get('AWS_S3_BUCKET_NAME')

CELERY_BROKER_URL = config.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config.get('CELERY_RESULT_BACKEND')