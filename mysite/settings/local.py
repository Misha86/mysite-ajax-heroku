"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)


from django.conf import settings

if settings.DEBUG:

    import os
    from django.utils.translation import ugettext_lazy as _

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    DEBUG = True

    ALLOWED_HOSTS = []

    # SMTP backend(default) for send email

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = 'smtp.gmail.com'                # Имя хоста используемое для отправки электронных писем. По умолчанию 'localhost'
    EMAIL_HOST_USER = 'yourgmail@gmail.com'      # Имя пользователя используемое при подключении к SMTP серверу указанному в EMAIL_HOST
    EMAIL_HOST_PASSWORD = 'yourpassword'         # Пароль для подключения к SMTP сервера, который указан в EMAIL_HOST
    EMAIL_SUBJECT_PREFIX = '[Django]'            # Префикс добавляемый к теме электронного письма
    EMAIL_PORT = 587                             # Порт, используемый при подключении к SMTP серверу указанному в EMAIL_HOST.
    EMAIL_USE_TLS = True                         # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 587 порт.
    # EMAIL_USE_SSL = False                        # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.
    # Обратите внимание, EMAIL_USE_TLS/EMAIL_USE_SSL взаимоисключающие, только одна настройка может быть True.                    # Указывает использовать ли TLS (защищенное) соединение с SMTP сервером. По умолчанию использует 465 порт.

    #6.18.1 Core Settings
    # ABSOLUTE_URL_OVERRIDES = {
    #     'blog.article': lambda o: "/article/%s/" % o.id,
    #     }

    DEFAULT_FROM_EMAIL = 'mishaelitzem2@rambler.ru'

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

    # Database
    # https://docs.djangoproject.com/en/1.8/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'django',                                     # Or path to database file if using sqlite3.
            'USER': 'postgres',
            'PASSWORD': '170986',
            'HOST': 'localhost',    # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',             # Set to empty string for default.
            'client_encoding': 'UTF8',
            }
    }

    # Internationalization
    # https://docs.djangoproject.com/en/1.8/topics/i18n/
    # 'ru-Ru'
    # 'uk-Uk'
    # 'en-En'

    # default language  (it don`t work if MIDDLEWARE_CLASSES have 'django.middleware.locale.LocaleMiddleware'
    #  and TEMPLATES have 'django.core.context_processors.i18n')

    LANGUAGE_CODE = 'uk-Uk'

    # list of languages
    LANGUAGES = (
        ('en', _('English')),
        ('uk', _('Ukraine')),
        ('ru', _('Russia')),
    )

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    TIME_ZONE = 'Europe/Kiev'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False

    from .db_password import db_password

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',   # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'django',                                     # Or path to database file if using sqlite3.
            'USER': 'postgres',
            'PASSWORD': db_password,
            'HOST': 'localhost',    # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '',             # Set to empty string for default.
        }
    }

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

    STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'static_root')

    MEDIA_URL = '/media/'

    MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'media_root')