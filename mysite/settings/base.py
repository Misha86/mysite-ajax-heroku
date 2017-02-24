"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants
from decouple import config, Csv
import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

SITE_ID = 1

# Настройка предусматривает отправку разработчикам сайта сообщений обо всех необработанных исключениях по электронной почте
ADMINS = [
    ("Михайло Поліщук", "mishaelitzem2@rambler.ru"),
    ]

#Кортеж по формату аналогичен ADMINS, который определяет кто получает оповещение о “сломанных” ссылках
MANAGERS = ADMINS

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # other django apps
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'django.contrib.redirects',
    'django.contrib.flatpages',
    'django.contrib.webdesign',   # for lorem
    'django.contrib.humanize',
    # third part
    'pagedown',
    'markdown_deux',
    # my apps
    'blog.apps.BlogConfig',
    'comment',
    'loginsys',
    'navigation',
    'languages',
)

MIDDLEWARE_CLASSES = (
    'log_request_id.middleware.RequestIDMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',     # Django может уведомлять вас о неработающих ссылках
    'django.middleware.locale.LocaleMiddleware',               # add this line after the SessionMiddleware for translate
    # 'django.middleware.cache.UpdateCacheMiddleware',         # add this line for cash all site
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.cache.FetchFromCacheMiddleware',        # add this line for cash all site
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',        # for REMOTE_USER
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # other MIDDLEWARE_CLASSES
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware'     # for redirects app
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'blog/templates/blog'),
                 os.path.join(BASE_DIR, 'blog/templates/blog/api'),
                 os.path.join(BASE_DIR, 'navigation/templates/navigation'),
                 os.path.join(BASE_DIR, 'comment/templates/comment'),
                 os.path.join(BASE_DIR, 'languages/templates/languages'),
                 os.path.join(BASE_DIR, 'loginsys/templates'),
                 os.path.join(BASE_DIR, 'loginsys/templates/registration')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',                  # add this processor for translate
                'django.core.context_processors.csrf',
                ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                    ]),
                ],
            },
        },
    ]

WSGI_APPLICATION = 'mysite.wsgi.application'

LANGUAGE_CODE = 'uk-Uk'

# list of languages
LANGUAGES = (
    ('en', _('English')),
    ('uk', _('Ukraine')),
    ('ru', _('Russia')),
)

DATABASES = {
    'default': {}
}

db_from_env = dj_database_url.config(conn_max_age=500)
if db_from_env:
    DATABASES['default'].update(db_from_env)
else:
    DATABASES['default'].update({
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': '',
        })

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'comment', 'static', 'comment'),
    os.path.join(BASE_DIR, 'loginsys', 'static', 'loginsys'),
    os.path.join(BASE_DIR, 'blog', 'static', 'blog'),
    os.path.join(BASE_DIR, 'languages', 'static', 'languages/img'),
)

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_root')

FIRST_DAY_OF_WEEK = 1

LOGIN_REDIRECT_URL = '/'

LOGIN_URL = '/auth/login/'

PASSWORD_RESET_TIMEOUT_DAYS = 1

MESSAGE_LEVEL = message_constants.DEBUG


# SMTP backend(default) for send email

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'                    # Имя хоста используемое для отправки электронных писем. По умолчанию 'localhost'
EMAIL_HOST_USER = "mpolishchuk1986@gmail.com"      # Имя пользователя используемое при подключении к SMTP серверу указанному в EMAIL_HOST
EMAIL_HOST_PASSWORD = '0967478910m'                 # Пароль для подключения к SMTP сервера, который указан в EMAIL_HOST
EMAIL_SUBJECT_PREFIX = '[Django]'              # Префикс добавляемый к теме электронного письма
EMAIL_PORT = 587                               # Порт, используемый при подключении к SMTP серверу указанному в EMAIL_HOST 2525.
EMAIL_USE_TLS = True                         # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 587 порт .
#EMAIL_USE_SSL = True                          # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.


LOGIN_URL = 'loginsys:login'                      # '/auth/login/'    It`s for @login_required().

LOGOUT_URL = 'loginsys:logout'                    # '/auth/logout/'

LOGIN_REDIRECT_URL = '/'

DEFAULT_FROM_EMAIL = 'mishaelitzem2@rambler.ru'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
    ]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
            }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

# AUTH_USER_MODEL = 'loginsys.MyUser'


# it`s settings for cash

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 20,
            'CULL_FREQUENCY': 2,
            }
    }
}

# it`s for cash all site

CACHE_MIDDLEWARE_SECONDS = 1800
CACHE_MIDDLEWARE_KEY_PREFIX = 'blog'

# Support for X-Request-ID

LOG_REQUEST_ID_HEADER = 'HTTP_X_REQUEST_ID'

LOG_REQUESTS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'request_id': {
            '()': 'log_request_id.filters.RequestIDFilter'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)-8s [%(asctime)s] [%(request_id)s] %(name)s: %(message)s'
        },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['request_id'],
            'formatter': 'standard',
            },
        },
    'loggers': {
        'log_request_id.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            },
        }
}


# отключить отчёты о 404 ошибке URL страницы заканчивается
import re
IGNORABLE_404_URLS = (
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
)

FIXTURE_DIRS = [os.path.join(BASE_DIR, 'navigation', 'fixtures', 'navigation')]