"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from .db import MYSQL
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-i3bp+_kdg9o=r4xys3lcq+8vi(nb_k2!e60%*fd-9li4*u#nv1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    # mis apps
    'apps.category',
    'apps.accounts'
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

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

#modelos de creacion de usuario que cree
AUTH_USER_MODEL = 'accounts.Account'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = MYSQL


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR, 'static')]
#media file
# MEDIA_ROOT=os.path.join(BASE_DIR,'media')
# no olvidar porner el MEDIA_URL al upload_to del modelo con archivo
MEDIA_URL='media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#configuracion para django azure storage
if 'WEBSITE_HOSTNAME' in os.environ: 
    azure_storage_blob = os.environ['AZURE_STORAGE_BLOB']
    azure_storage_blob_parametros = {parte.split(' = ')[0]:parte.split(' = ')[1] for parte in azure_storage_blob.split('  ')}
else:
    azure_storage_blob_parametros = {'account_name':os.environ.get('ACCOUNT_NAME'),
                                     'container_name':os.environ.get('CONTAINER_NAME'),
                                     'account_key':os.environ.get('ACCOUNT_KEY')}

AZURE_CONTAINER = azure_storage_blob_parametros['container_name']
AZURE_ACCOUNT_NAME = azure_storage_blob_parametros['account_name']
AZURE_ACCOUNT_KEY = azure_storage_blob_parametros['account_key']
STORAGES = {
    "default": {"BACKEND": "storages.backends.azure_storage.AzureStorage"},
    "staticfiles": {"BACKEND": "custom_storage.custom_azure.PublicAzureStaticStorage"},
    "media": {"BACKEND": "custom_storage.custom_azure.PublicAzureMediaStorage"},
}
