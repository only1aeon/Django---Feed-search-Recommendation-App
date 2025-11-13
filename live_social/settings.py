import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY','changeme')
DEBUG = os.environ.get('DEBUG','0') in ('1','True','true')
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = [
    'django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles',
    'rest_framework','recommendations','users'
]
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware']
ROOT_URLCONF = 'live_social.urls'
TEMPLATES = []
WSGI_APPLICATION = 'live_social.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2', 'NAME': os.environ.get('POSTGRES_DB','live_social'), 'USER': os.environ.get('POSTGRES_USER','postgres'), 'PASSWORD': os.environ.get('POSTGRES_PASSWORD','postgres'), 'HOST': os.environ.get('DB_HOST','db'), 'PORT': os.environ.get('DB_PORT','5432')}}
STATIC_URL = '/static/'
