"""
Django settings for django_messenger_project project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

from celery.schedules import crontab

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-fn0ml70ie$&o$4ut21@u9ju&#iy_68q3s^w=-l@abb@0%4t&0z'

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
    # 'messenger_app',
    'messenger_app.apps.MessengerAppConfig',
    'rest_framework',
    'api_app.apps.ApiAppConfig',
    'celery',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'messenger_app.middleware.UpdateLastActivityMiddleware',

]

ROOT_URLCONF = 'django_messenger_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        # 'DIRS': []
    ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'messenger_app.context_processors.random_color'
            ],
        },
    },
]

WSGI_APPLICATION = 'django_messenger_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "messenger",
        "USER": "superuser",
        "PASSWORD": "",
        "HOST": "psql_db",
        "PORT": "5432",
    }
}


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

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}
# Час життя сесії у секундах (наприклад, 15 хвилин)
SESSION_COOKIE_AGE = 1800

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_SAVE_EVERY_REQUEST = True

SESSION_COOKIE_SECURE = False

MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"

CELERY_BROKER_URL = 'redis://redis:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

CELERYD_LOG_LEVEL = 'INFO'
CELERYD_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
CELERYD_TASK_LOG_FORMAT = '[%(asctime)s: %(levelname)s/%(processName)s] Task %(task_name)s[%(task_id)s]: %(message)s'

CELERY_BEAT_SCHEDULE = {
    'log-last-10-messages-every-5-minutes': {
        'task': 'messenger_app.tasks.log_last_10_messages',
        'schedule': 300.0,
    },
    'print_chats_profiles': {
        'task': 'messenger_app.tasks.print_chats_profiles',
        'schedule': 300.0,
    }
}
