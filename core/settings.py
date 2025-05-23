"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/

"""

import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DJANGO_DEBUG", "FALSE") == "TRUE"
# DEBUG = True
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")

# CSRF settings
CSRF_TRUSTED_ORIGINS = os.getenv(
    "DJANGO_CSRF_TRUSTED_ORIGINS", "https://nepal.gnome.org"
).split(",")
CSRF_COOKIE_SECURE = not DEBUG  # Send cookies over HTTPS in production
CSRF_COOKIE_SAMESITE = "Lax"  # Restrict cookies to same-site requests
# Application definition

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third party apps
    "drf_yasg",
    "celery",
    "rest_framework",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "django_summernote",
    # django apps
    # todo
    "newsletter",
    "faq",
    "event",
    "nested_admin",
    "healthcheck",
    "chatbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"
CORS_ALLOW_ALL_ORIGINS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"
ASGI_APPLICATION = 'core.asgi.application'


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        # Set to empty string for localhost
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),  # Set to empty string for default
    },
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation." "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "prefix": "Bearer",
        }
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_TIMEZONE = "Asia/Kathmandu"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60 * 60 * 2
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"


STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {},
    },
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv("STATIC_ROOT", "staticfiles"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT", "media"))


# Logs

LOG_DIR = BASE_DIR / os.getenv("LOG_PATH", "logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        # Console output handler
        "console": {
            "class": "logging.StreamHandler",
        },
        # File handler for synchronization log with dynamic filename
        "file_sync": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": rf"{LOG_DIR}/custom.log",
            "when": "D",  # Rotate daily
            "interval": 1,  # Every 1 day
            "backupCount": 5,  # Keep 5 backups
            "formatter": "verbose",
        },
        # File handler for SQL log with dynamic filename and daily rotation
        "file_sql": {
            "level": "DEBUG",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": rf"{LOG_DIR}/sql.log",
            "when": "D",  # Rotate daily
            "interval": 1,  # Every 1 day
            "backupCount": 5,  # Keep 5 backups
            "formatter": "verbose",
        },
        # File handler for Django standard error logs
        "file_django_error": {
            "level": "ERROR",
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": rf"{LOG_DIR}/django_error.log",
            "when": "D",  # Rotate daily
            "interval": 1,  # Every 1 day
            "backupCount": 5,  # Keep 5 backups
            "formatter": "django.server",
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(message)s",
        },
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        },
    },
    "loggers": {
        # Logger for synchronization system
        "CUSTOM_LOG": {
            "handlers": ["file_sync", "console"] if DEBUG else ["file_sync"],
            "level": "INFO" if DEBUG else "CRITICAL",
            "propagate": False,
        },
        # Logger for SQL queries
        "django.db.backends": {
            "handlers": ["file_sql"],
            "level": "DEBUG",
            "propagate": False,
        },
        # Logger for Django standard error
        "django.request": {
            "handlers": ["file_django_error"],
            "level": "ERROR",
            "propagate": False,
        },
    },
}

JAZZMIN_SETTINGS = {
    "show_ui_builder": True,
}
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": "480",
        "toolbar": [
            ["style", ["style"]],
            ["font", ["bold", "italic", "underline", "clear"]],
            ["fontname", ["fontname"]],
            ["color", ["color"]],
            ["para", ["ul", "ol", "paragraph"]],
            ["table", ["table"]],
            ["insert", ["link", "picture", "video"]],
            ["view", ["fullscreen", "codeview"]],
        ],
    },
    # Require users to be authenticated for uploading attachments.
    "attachment_require_authentication": True,
    # Set custom storage class for attachments.
    "attachment_storage_class": (
        "django.core.files.storage.FileSystemStorage"
    ),
    # Set to `False` to return attachment paths in relative URIs.
    "attachment_absolute_uri": True,
}


MIGRATION_MODULES = {
    "django_summernote": "summernote.migrations",
}
