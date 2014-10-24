"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^$p8qro2lr+7b-cm0vaccv9k$u+r1hvy874&krrtx8n4z1mw7('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'grumblr',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Configures Django to merely print emails rather than sending them.
# Comment out this line to enable real email-sending.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# To enable real email-sending, you should uncomment and
# configure the settings below.
# EMAIL_HOST = 'Your-SMTP-host'               # perhaps 'smtp.andrew.cmu.edu'
# EMAIL_HOST_USER = 'Your-SMTP-username'      # perhaps your Andrew ID
# EMAIL_HOST_PASSWORD = 'Your-SMTP-password'
# EMAIL_USE_TLS = True

ROOT_URLCONF = 'webapps.urls'

# URL to use if the authentication system requires a user to log in.
LOGIN_URL = '/login'

# Default URL to redirect to after a user logs in.
LOGIN_REDIRECT_URL = '/homepage'



WSGI_APPLICATION = 'webapps.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'grumblr',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'webapps',
        'PASSWORD': 'fun',
        'HOST': 'localhost',    # Empty for localhost through domain sockets or           '127.0.0.1' for localhost through TCP.
        'PORT': '',             # Set to empty string for default.
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
