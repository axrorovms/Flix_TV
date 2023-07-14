from datetime import timedelta
from typing import List, Tuple

from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = ['*']

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_yasg',
    'mptt',
    'django_countries',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'django_minio_backend'
]

LOCAL_APPS = [
    'user',
    'movie',
    'dashboard',
    # 'elastic_search.apps.ElasticSearchConfig'
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'
AUTH_USER_MODEL = 'user.User'

DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('POSTGRES_DB', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('POSTGRES_PORT')
    }
}


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

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST_FRAMEWORK = {
#     'DEFAULT_PAGINATION_CLASS':
#     'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 25,
#     'ORDERING_PARAM': 'ordering',
# }

# Elasticsearch configuration
ELASTICSEARCH_DSL = {
    'default': {
        'hosts': 'localhost:9200'
    },
}

# Minio

MINIO_EXTERNAL_ENDPOINT = "127.0.0.1:9000"
MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = False
MINIO_ENDPOINT = 'minio:9000'
MINIO_ACCESS_KEY = 'minio'
MINIO_SECRET_KEY = 'minio123'
MINIO_USE_HTTPS = False
MINIO_PRIVATE_BUCKETS = [
    "test"
]
MINIO_PUBLIC_BUCKETS = [
    "images",
    "videos"
]
# MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []

MINIO_URL_EXPIRY_HOURS = timedelta(days=1)
MINIO_MEDIA_FILES_BUCKET = 'test'


# SMTP settings
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
