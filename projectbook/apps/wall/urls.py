
from django.conf.urls.defaults import *
from django.views.generic import DetailView, ListView

from projectbook.apps.wall.models import Post

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Post.objects.order_by('-pub_date')[:5],
            context_object_name='latest_post_list',
            template_name='index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Post,
            template_name='detail.html')),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Post,
            template_name='results.html'),
        name='post_results'),
    url(r'^(?P<posts_id>\d+)/vote/$', 'posts.views.vote'),
)
