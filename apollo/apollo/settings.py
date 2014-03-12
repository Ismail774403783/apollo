"""
Django settings for apollo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import urlparse
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
ugettext = lambda s: s


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'SOMETHING_SECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'core',
    'accounts',
    'messaging',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'mongoengine.django.mongo_auth',
    'pipeline',
)

MIDDLEWARE_CLASSES = (
    'core.middleware.DeploymentMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'apollo.urls'

WSGI_APPLICATION = 'apollo.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'mongoengine.django.auth.MongoEngineBackend',
)
AUTH_USER_MODEL = 'mongo_auth.MongoUser'
MONGOENGINE_USER_DOCUMENT = 'accounts.documents.User'

SESSION_ENGINE = 'mongoengine.django.sessions'
SESSION_SERIALIZER = 'mongoengine.django.sessions.BSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Support for LXC-based containers
if os.environ.get('container') == 'lxc':
    MONGO_ENV_NAME = 'MONGODB_PORT'
else:
    MONGO_ENV_NAME = 'MONGO_DATABASE_HOST'

MONGO_DATABASE_HOST = urlparse.urlparse(
    os.environ.get(MONGO_ENV_NAME, 'mongodb://localhost')).netloc
MONGO_DATABASE_NAME = os.environ.get('MONGO_DATABASE_NAME', 'apollo')


from mongoengine import connection
try:
    connection.connect(MONGO_DATABASE_NAME, host=MONGO_DATABASE_HOST)
except connection.ConnectionError:
    pass

# Testing
TEST_RUNNER = 'core.utils.test.MongoEngineTestSuiteRunner'
TEST_RUNNER_FILTER = (
    'core',
    'messaging'
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', ugettext('English')),
    ('az', ugettext('Azerbaijani')),
    ('fr', ugettext('French')),
)

TIME_ZONE = os.environ.get('TIMEZONE', 'UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/assets/'
PIPELINE_CSS = {
    'apollo': {
        'source_filenames': (
            'core/css/bootstrap.css',
            'core/css/select2.css',
            'core/css/table-fixed-header.css',
            'core/css/datepicker.css',
            'core/css/jquery.qtip.css',
            'core/css/custom.css',
        ),
        'output_filename': 'css/apollo.css',
        'extra_context': {
            'media': 'screen,projection',
        },
    },
}

PIPELINE_JS = {
    'apollo': {
        'source_filenames': (
            'core/js/jquery.js',
            'core/js/bootstrap.js',
            'core/js/select2.js',
            'core/js/table-fixed-header.js',
            'core/js/bootstrap-datepicker.js',
            'core/js/custom.js',
        ),
        'output_filename': 'js/apollo.js',
    },
    'graphs': {
        'source_filenames': (
            'js/underscore.js',
            'js/jquery.csv.js',
            'js/raphael.js',
            'js/jquery.qtip.js',
            'js/kartograph.js',
        ),
        'output_filename': 'js/graphs.js',
    }
}

# Messaging
ALLOWED_PUNCTUATIONS = '!'  # allowed punctuations in SMS forms
CHARACTER_TRANSLATIONS = (
    ('i', '1'),
    ('I', '1'),
    ('o', '0'),
    ('O', '0'),
    ('l', '1'),
    ('L', '1'),
)
