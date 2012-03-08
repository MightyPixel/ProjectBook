from django.conf.urls.defaults import *


urlpatterns = patterns('',
    url(r'^admin/calendar/$', 'projectbook.apps.project_calendar.admin_views.index' , name="home_calendar"),
    url(r'^admin/arrange/$', 'projectbook.apps.project_calendar.admin_views.create_events'),
)
