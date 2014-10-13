from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^sio/', include('sio.urls')),
    url(r'^$', 'sio.views.home'),
)
