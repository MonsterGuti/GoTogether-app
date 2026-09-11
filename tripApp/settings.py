"""
Django settings for tripApp project.
"""

from pathlib import Path
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security & Debug Settings
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-+hqoe4rceqvhse$qdlhor5*l1bja&q6u8375y07mp)pa$ulicc')
DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['takethetripapp.com', 'www.takethetripapp.com', 'localhost', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = [
    'https://takethetripapp.com',
    'https://www.takethetripapp.com',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Custom Apps
    'rides',
    'users',
    'reviews',
    'notifications',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tripApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.context_processors.unread_notifications',
            ],
        },
    },
]

WSGI_APPLICATION = 'tripApp.wsgi.application'

# Custom User Model
AUTH_USER_MODEL = 'rides.User'

# Database Configuration (Настроено за TakeTheTrip в DigitalOcean)
DATABASES = {
    'default': dj_database_url.config(
        default="postgres://monsterguti:marti123@127.0.0.1:5432/takethetrip",
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'bg'
TIME_ZONE = 'Europe/Sofia'
USE_I18N = True
USE_TZ = True

# Static & Media files
STATIC_URL = '/static/'

STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Authentication Redirects
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'takethetripapp@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'igcbnbnejppuynyz')

DEFAULT_FROM_EMAIL = 'TakeTheTrip <takethetripapp@gmail.com>'
SITE_URL = 'http://165.22.16.47'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'