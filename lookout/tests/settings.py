
""" Django settings for running tests with the standalone app Django-Lookout. """

import tempfile


ROOT_URLCONF = 'lookout.tests.urls'

SECRET_KEY = 'testtesttesttest'

DEBUG = False

MEDIA_ROOT = tempfile.mkdtemp()
MEDIA_URL = '/media/'

STATIC_ROOT = tempfile.mkdtemp()
STATIC_URL = '/static/'

ALLOWED_HOSTS = ['*']

USE_TZ = True

INSTALLED_APPS = (
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.auth',
	'django.contrib.staticfiles',
	'lookout',
	'lookout.tests',
)

MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
)

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': ':memory:',
		'TEST_CHARSET': 'utf8'
	}
}

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'APP_DIRS': True
	}
]
