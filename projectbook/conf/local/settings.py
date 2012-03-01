from projectbook.conf.settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SOUTH_TESTS_MIGRATE = False

ADMINS = (
    ('You', 'your@email'),
)
MANAGERS = ADMINS

ADMIN_TOOLS_MENU = 'projectbook.menu.CustomMenu'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(VAR_ROOT, 'dev.db'),
    }
}

ROOT_URLCONF = '%s.conf.local.urls' % PROJECT_MODULE_NAME

FIXTURE_DIRS = (
   os.path.join(VAR_ROOT,'fixtures')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    # default template context processors
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',

    'django.core.context_processors.request',
)

INSTALLED_APPS += (
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'django_evolution',
    
    'projectbook.apps.project_arrange',
    'projectbook.apps.project_calendar',
)
