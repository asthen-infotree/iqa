"""
Django settings for certificate project.

Generated by 'django-admin startproject' using Django 4.2.

For more information on this files, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
DEV_MODE = os.getenv('DEV_MODE')

ALLOWED_HOSTS = ['ikramqa.azurewebsites.net']

SITE_ID=1
# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'certificate',
    # 'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'crispy_forms',
    "crispy_bootstrap5",
    'cities_light',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'django_summernote',
    'frontend_settings',
    'bootstrap5',
    'datatableview',
    'corsheaders',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

CITIES_LIGHT_INCLUDE_COUNTRIES = ['MY']

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email"
        ],
        "AUTH_PARAMS":{"access_type": "online"}
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'allauth.account.middleware.AccountMiddleware'
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'ikramqa.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ikramqa.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('DBNAME'),
            'USER': os.getenv('DBUSER'),
            'PASSWORD': os.getenv('DBPASS'),
            'HOST': os.getenv('DBHOST'),
            'PORT': '5432',
        }
    }

AUTH_USER_MODEL = 'users.CustomUser'
# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_TZ = True

USE_L10N = False

# from django.conf.locale.en import formats as en_formats
#
# en_formats.DATE_FORMAT = "d/M/Y"

DATE_INPUT_FORMATS = (('%d.%m.%Y'),)
# DATETIME_FORMAT = (('d-m-Y H:i'))
# DATETIME_INPUT_FORMATS = (('%d-%m-%Y %H:%i'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/



STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")

# print("Templates", os.path.join(BASE_DIR, 'templates'))
# STATIC_URL = 'https://ikramqa-c0egghawdcgndzgg.z01.azurefd.net/static/'
MEDIA_URL = '/media/'
# MEDIA_URL = 'https://ikramqa-c0egghawdcgndzgg.z01.azurefd.net/media/'
# MEDIA_ROOT= 'ikramqa-c0egghawdcgndzgg.z01.azurefd.net/media/'

# DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
# AZURE_ACCOUNT_NAME = 'djangoazure'
# AZURE_CONTAINER = 'static'

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": 'media',
            "account_key": config('ACCOUNT_KEY'),
            "account_name": config('ACCOUNT_NAME'),
            "overwrite_files" : True,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
        "OPTIONS": {
            "azure_container": 'static',
            "account_key": config('ACCOUNT_KEY'),
            "account_name": config('ACCOUNT_NAME'),
            }
    },
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend"
)

LOGIN_REDIRECT_URL = "/portal"
LOGOUT_REDIRECT_URL = "/"

import mimetypes
mimetypes.add_type("text/css", ".css", True)


SOCIALACCOUNT_LOGIN_ON_GET=True