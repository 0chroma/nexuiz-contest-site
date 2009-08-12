from django.conf.urls.defaults import *

urlpatterns = patterns('',
   (r'^(?P<user_id>\d+)/$', 'contest.apps.users.views.user'),
   
   (r'^accounts/login/$', 'django.contrib.auth.views.login'),
   ('^accounts/logout/$', 'django.contrib.auth.views.logout'),
   ('^accounts/password_change/$', 'django.contrib.auth.views.password_change'),
   ('^accounts/password_change/done/$', 'django.contrib.auth.views.password_change_done'),
)