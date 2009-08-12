from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^$', 'contest.apps.contests.views.index'),
   (r'^(?P<contest_id>\d+)/$', 'contest.apps.contests.views.detail'),
   
   (r'^entry/(?P<entry_id>\d+)/$', 'contest.apps.contests.views.entry'),
   
   (r'^judge/$', 'contest.apps.contests.views.judge'),
   
   (r'^rules/$', 'contest.apps.contests.views.rules'),
   
   (r'^submit/$', 'contest.apps.contests.views.submit'),
   
   (r'^users/(?P<user_id>\d+)/$', 'contest.apps.contests.views.user'),
   
   (r'^accounts/login/$', 'django.contrib.auth.views.login'),
   ('^accounts/logout/$', 'django.contrib.auth.views.logout'),
   ('^accounts/password_change/$', 'django.contrib.auth.views.password_change'),
   ('^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done'),
)