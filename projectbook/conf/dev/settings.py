from projectbook.conf.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = 'projectbook.conf.dev.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'projectbook',
#        'USER': 'dbuser',
#        'PASSWORD': 'dbpassword',
    }
}

print VAR_ROOT

INSTALLED_APPS += (
    'django.contrib.admin',
    'django.contrib.admindocs',
)
