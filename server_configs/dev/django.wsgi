import os, sys
import site

site.addsitedir('/opt/webapps/projectbook/lib/python2.5/site-packages')


sys.stdout = sys.stderr

os.environ['DJANGO_SETTINGS_MODULE'] = 'projectbook.conf.local.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
