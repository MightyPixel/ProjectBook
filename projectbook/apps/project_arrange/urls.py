from django.conf.urls.defaults import *


## calendar view
urlpatterns = patterns('projectbook.apps.project_arrange.views',
    url(r'^index/$' , 'index'),
    url(r'^arrange/$' , 'arrange'),
    
)
