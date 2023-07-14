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
    'mptt',
    'django_countries',
    'django_elasticsearch_dsl',
    'django_elasticsearch_dsl_drf',
    'django_minio_backend'
    'drf_yasg',
    'djoser'
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
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')

# REST_FRAMEWORK
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'

    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": os.getenv('SECRET_KEY'),
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ('Bearer',),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=10),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

DJOSER = {
    # Login and Logout Settings
    'LOGIN_FIELD': 'username',
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    # __________________________________________________

    # USERNAME AND PASSWORD RESET-CONFIRM-URL
    'PASSWORD_RESET_CONFIRM_URL': '/password-reset/{uid}/{token}',
    'USERNAME_RESET_CONFIRM_URL': '/username-reset/{uid}/{token}',
    # __________________________________________________

    'SEND_ACTIVATION_EMAIL': False,
    # Agar Truefoydalanuvchi quyidagidan keyin elektron pochta orqali yuborilgan faollashtirish havolasini bosishi talab etilsa:
    'SEND_CONFIRMATION_EMAIL': False,
    # Agar bo'lsa True, ro'yxatdan o'tish yoki faollashtirish so'nggi nuqtasi foydalanuvchiga tasdiqlovchi xat yuboradi.
    # __________________________________________________

    # USERNAME PASSWORD CHANGED-EMAIL-CONFIRMATION
    # Agar “True”ga sozlangan boʻlsa, parolni oʻzgartirish soʻnggi
        # nuqtalari foydalanuvchiga tasdiqlovchi xat yuboradi.
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,
    # Agar “True”ga sozlangan boʻlsa, username oʻzgartirish soʻnggi
        # nuqtalari foydalanuvchiga tasdiqlovchi xat yuboradi.
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,
    # __________________________________________________
    'ACTIVATION_URL': '/activate/{uid}/{token}',
    #Agar bo'lsa , parol tengligini tekshirish uchun oxirgi
        # nuqtaga o'tishingiz Truekerak .re_password/users/
    'USER_CREATE_PASSWORD_RETYPE': False,
    # __________________________________________________
    # SET USERNAME-OR-PASSWORD RETYPE
    # Agar bo'lsa , foydalanuvchi nomi tengligini tasdiqlash uchun oxirgi nuqtaga o'tishingiz
        # True kerak .re_new_username/users/set_username/
    'SET_USERNAME_RETYPE':False,
    # Agar bo'lsa , parol tengligini tekshirish uchun oxirgi nuqtaga o'tishingiz
        # True kerak .re_new_password/users/set_password/
    'SET_PASSWORD_RETYPE':False,
    # __________________________________________________

    # USERNAME OR PASSWORD RESET CONFIRM RETYPE
    # Agar bo'lsa , parol tengligini tekshirish uchun oxirgi nuqtaga o'tishingiz
        # True kerak .re_new_password/users/reset_password_confirm/
    'PASSWORD_RESET_CONFIRM_RETYPE': False,
    # Agar bo'lsa , foydalanuvchi nomi tengligini tasdiqlash uchun oxirgi nuqtaga o'tishingiz
        # True kerak .re_new_username/users/reset_username_confirm/
    'USERNAME_RESET_CONFIRM_RETYPE': False,
    # __________________________________________________
    # USERNAME OR PASSWORD  RESET_SHOW_EMAIL_NOT_FOUND
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'USERNAME_RESET_SHOW_EMAIL_NOT_FOUND': False,
    'SERIALIZER': {

    }
}

SWAGGER_SETTINGS = {
    'VALIDATOR_URL': 'http://localhost:8189',
    'DEFAULT_INFO': 'import.path.to.urls.api_info',
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Type in the *\'Value\'* input box below: **\'Bearer &lt;JWT&gt;\'**, '
                           'where JWT is the JSON web token you get back when logging in.'
        }
    }

}