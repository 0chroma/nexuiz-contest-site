from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^contest/', include('contest.apps.foo.urls.foo')),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'media'}),
    (r'^uploads/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'uploads'}),
    
    (r'^$', include("contest.apps.news.urls")),
    (r'^news/', include("contest.apps.news.urls")),
    
    (r'^contests/', include("contest.apps.contests.urls")),
    (r'^user/', include("contest.apps.users.urls")),
    (r'^admin/', include('django.contrib.admin.urls')),
)
