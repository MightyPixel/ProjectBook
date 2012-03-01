from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    url(r'^admin/calendar/$', 'projectbook.apps.project_calendar.admin_views.index'),
    url(r'^admin/arrange/$', 'projectbook.apps.project_calendar.admin_views.create_events'),

    url(r'^admin_tools/', include('admin_tools.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': '/Users/pixel/Sites/Python/projectbook/py_venv/var/static'}),
    
    url(r'^projects/' , include('projectbook.apps.project_arrange.urls')),
    url(r'^calendar/' , include('projectbook.apps.project_calendar.urls')),
)
