from .base import *
BASE_DIR = Path(__file__).resolve().parent.parent.parent


DOTENV_FILE=f'{BASE_DIR}/.env.test'
config = Config(RepositoryEnv(DOTENV_FILE))
DEBUG = False

ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config.get('DB_NAME'),
        'USER': config.get('DB_USER'),
        'PASSWORD': config.get('DB_PASSWORD'),
        'HOST': config.get('DB_HOST'),
        'PORT': config.get('DB_PORT'),
    }
}