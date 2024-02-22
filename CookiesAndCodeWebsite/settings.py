"""
Django settings for CookiesAndCodeWebsite project.
Generated by 'django-admin startproject' using Django 4.0.3.
For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os 
from os import environ
from dotenv import load_dotenv
import dj_database_url
load_dotenv()
import logging

# Add logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
logger = logging.getLogger(__name__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# run 'export DEBUG_VALUE="True"' from terminal to develop locally
DEBUG = (os.environ.get('DEBUG_VALUE') == "True")
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = os.environ.get('WEBSITE_EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('WEBSITE_EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'Cookies & Code Password Change'


# Application definition

INSTALLED_APPS = [
    #'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_extensions",
    'active_link',
    'main'

]

AUTH_USER_MODEL = 'main.CustomUser'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'CookiesAndCodeWebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join("BASE_DIR", 'main', 'templates', 'main')],
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

WSGI_APPLICATION = 'CookiesAndCodeWebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default':  {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    "bk_local": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'candctu',
        'USER': 'bennett',
        'PASSWORD': 'django_tut_you_cant_guess123',

        'HOST': 'localhost',
        'PORT': '5432',
    },
    "bk_local_1": {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'databasename',
        'USER': 'bennett',
        'PASSWORD': 'django_tut_you_cant_guess123',

        'HOST': 'localhost',
        'PORT': '5432',
    }
}
db_from_env = dj_database_url.config(conn_max_age=500)
logger.info(f'Database configuration from environment: {db_from_env}')
DATABASES['default'].update(db_from_env)


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_TZ = True

# django_project/settings.py
LOGIN_REDIRECT_URL = "/home" # page you're redirected to when you logout
LOGOUT_REDIRECT_URL = "/home" # page you're redirected to when you logout
LOGIN_URL = "/home" # page you're redirected to when you logout


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATIC_URL = "static/"
STATICFILES_STORAGE = "whitenoise.storage.CompresesdManifestStaticFilesStorage"
STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'staticfiles')
]




import django_heroku
django_heroku.settings(locals())

if os.getcwd() == '/app':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
