from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^home$', 'sio.views.home'),
    # will add routes later for add student / add course / register actions
)
