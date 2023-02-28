import os
from pathlib import Path

import pretty_errors
from decouple import config
from dj_database_url import parse as db_url

pretty_errors.configure(
    separator_character='*',
    filename_display=pretty_errors.FILENAME_EXTENDED,
    line_number_first=True,
    display_link=True,
    lines_before=5,
    lines_after=2,
    line_color=f'{pretty_errors.RED}> {pretty_errors.default_config.line_color}',
    code_color=f'  {pretty_errors.default_config.line_color}',
    truncate_code=True,
    display_locals=True,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'ckeditor',
    'django_extensions',
    # 'silk',
    'ratelimit',

    'rest_auth',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'silk.middleware.SilkyMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        cast=db_url
    )
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Baghdad'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'build/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "static"),
# ]
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
SITE_ID = 1

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SILKY_AUTHENTICATION = True  # User must login
# SILKY_AUTHORISATION = True  # User must have permissions
# SILKY_ANALYZE_QUERIES = True
# SILKY_META = True

SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_ANALYZE_QUERIES = True
SILKY_PYTHON_PROFILER_RESULT_PATH = 'profile/'

CORS_ALLOW_ALL_ORIGINS = True

# Use as your requirements
AUTH_USER_MODEL = 'rest_auth.EmailAccount'

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60 * 24


# LOGGING = {
#     'version': 1,
#     'formatters': {
#         'mosayc': {
#             'format': '%(asctime)-15s %(levelname)-7s %(message)s [%(funcName)s (%(filename)s:%(lineno)s)]',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'mosayc'
#         }
#     },
#     'loggers': {
#         'silk': {
#             'handlers': ['console'],
#             'level': 'DEBUG'
#         }
#     },
# }