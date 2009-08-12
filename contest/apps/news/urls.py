from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^$', 'contest.apps.news.views.index'),
   (r'^(?P<id>\d+)/$', 'contest.apps.news.views.item'),
)