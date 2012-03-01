from projectbook.conf.settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

print "hello-----------------"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

print VAR_ROOT


ROOT_URLCONF = 'projectbook.conf.test.urls'

INSTALLED_APPS += ('django_nose',)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

