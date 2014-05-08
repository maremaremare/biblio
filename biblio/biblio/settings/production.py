"""Production settings and globals."""


from os import environ

from base import *

from secrets import SECRET_KEY, DB_PASS, EMAIL_PASS


# HOST CONFIGURATION
# See:
# https://docs.djangoproject.com/en/1.5/releases/1.5/#allowed-hosts-required-in-production
ALLOWED_HOSTS = ['krotov.land', 'biblio.land']
# END HOST CONFIGURATION

# EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_HOST_USER = 'shop@biblio.land'
EMAIL_HOST_PASSWORD = EMAIL_PASS
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tl
# END EMAIL CONFIGURATION
STATICFILES_DIRS = (
    '/home/maremare/domains/' + SITE_DOMAIN_NAME + '/static/',
)
STATIC_ROOT = '/home/maremare/domains/' + SITE_DOMAIN_NAME + '/static/root/'
MEDIA_ROOT = '/home/maremare/domains/' + SITE_DOMAIN_NAME + '/media/'
# DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'biblio',
        'USER': 'django_login',
        'PASSWORD': DB_PASS,
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
# END DATABASE CONFIGURATION


# CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
#CACHES = {}
# END CACHE CONFIGURATION
