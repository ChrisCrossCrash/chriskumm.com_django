"""
Django settings for drf_project project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import logging.config
from pathlib import Path

# noinspection PyPackageRequirements
from decouple import config

from drf_project.custom_logging import CUSTOM_LOGGING

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# Site Name (used in admin page header, and available for other things)
SITE_NAME = "Chris Kumm Web Designs"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', cast=bool)

ALLOWED_HOSTS = [
    f'.{config("DOMAIN_NAME")}',
]

if DEBUG:
    ALLOWED_HOSTS.extend([
        '127.0.0.1',
        'localhost',
        'testserver',
    ])


# Application definition

INSTALLED_APPS = [
    # Django Admin Interface
    'admin_interface',
    'colorfield',

    # Default
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # This project
    'core.apps.CoreConfig',

    # Third-party
    'rest_framework',
    'corsheaders',
    'ckeditor',
]

MIDDLEWARE = [
    # For Django CORS Headers
    'corsheaders.middleware.CorsMiddleware',

    # Default
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'drf_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
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

WSGI_APPLICATION = 'drf_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Override the default User model
# https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project

AUTH_USER_MODEL = 'core.CoreUser'


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = config('TIME_ZONE')

USE_I18N = False

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/django/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# HTTPS Settings
# https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/#https

if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True


# Email
# https://docs.djangoproject.com/en/3.1/topics/email/#email-backends
# EMAIL_HOST = 'email-smtp.us-east-2.amazonaws.com'
# EMAIL_PORT = 587
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
# EMAIL_USE_TLS = True

# default SERVER_EMAIL is root@localhost
SERVER_EMAIL = f'django@{config("DOMAIN_NAME")}'

# By default, admins are sent error emails when DEBUG is False
ADMINS = [
    ('Chris', 'chrislkumm@protonmail.com'),
]

MANAGERS = [
    ('Chris', 'chrislkumm@protonmail.com'),
]

if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# Logging
# https://docs.djangoproject.com/en/3.0/topics/logging/#module-django.utils.log

# Disable django default logging configuration.
LOGGING_CONFIG = None

# Load and enable a custom logging configuration for this project.
logging.config.dictConfig(CUSTOM_LOGGING)


# CKEditor
# https://django-ckeditor.readthedocs.io/en/latest/#optional-customizing-ckeditor-editor

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Custom',
        'toolbar_Custom': [
            ['Format'],
            ['Bold', 'Italic', 'Underline'],
            ['TextColor', 'BGColor'],
            ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'JustifyLeft', 'JustifyCenter', 'JustifyRight'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'SpecialChar', 'HorizontalRule'],
            ['Scayt'],
            ['RemoveFormat', 'Source']
        ]
    }
}


# This is required for Django Admin Interface to work properly.
# https://github.com/ChrisCrossCrash/django-admin-interface#installation

X_FRAME_OPTIONS = 'SAMEORIGIN'


# Django CORS Headers
# https://github.com/adamchainz/django-cors-headers#configuration

CORS_ALLOW_ALL_ORIGINS = DEBUG
