
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': '/Users/pixel/Sites/Python/projectbook/py_venv/var/static'}),

    url(r'^' , include('projectbook.apps.wall.urls')),    
    url(r'^projects/' , include('projectbook.apps.project_arrange.urls')),
    url(r'^calendar/' , include('projectbook.apps.project_calendar.urls')),
)

