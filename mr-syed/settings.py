import django_heroku
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.mr-syed.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&b5=0pq&c-#18rpqb92v7h%9h4xd%l!*9*j2y4bq5cgpnmv6*d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# ALLOWED_HOSTS = ['3.134.92.56']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "storages",
    'django.contrib.staticfiles',
    # local apps
    'home',
    'accounts',
    'exams',
    'questions',
    "classes",
    "homework",
    "lectures",
    # 3rd Party
    'django_crontab',


]
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mr-syed.urls'

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

WSGI_APPLICATION = 'mr-syed.wsgi.application'


# Database
# https://docs.mr-syed.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.mr-syed.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.mr-syed.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.mr-syed.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'
AUTH_USER_MODEL = 'accounts.CustomUser'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MEDIA_URL = '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mr.sayedabdelhamed@gmail.com'
EMAIL_HOST_PASSWORD = 'iszoleqzpvimtcre'  # past the key or password app here
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'default from email'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
django_heroku.settings(locals())


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Cairo'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = 'AKIAQKW72FGFKP7AXDV4'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'mr-sayedabdelhamed2'
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = 'public-read'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_S3_ENDPOINT_URL = 'https://s3-us-west-2.amazonaws.com'
CRONJOBS = [
    ('59 23 * * *', 'accounts.cron.deactivate_users')
]

ADMINS = (
    ('yasser', 'yasser.aboelgheit@gmail.com')
)

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'simple': {
#             'format': '%(levelname)s | %(message)s'
#         },
#     },
#     'handlers': {
#         # 'console': {
#         #     'level': 'DEBUG',
#         #     'class': 'logging.StreamHandler',
#         #     'formatter': 'simple'
#         # },
#         # 'mail_admins': {
#         #     'level': 'DEBUG',
#         #     'class': 'django.utils.log.AdminEmailHandler'
#         # },
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR + '/logs/debug.log',
#             "formatter": "simple",
#         },
#     },

#     'loggers': {
#         'requests': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },

#     },
# }
