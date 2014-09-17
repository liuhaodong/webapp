from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^homepage$', 'grumblr.views.homepage'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^registration$', 'grumblr.views.registration'),
)
