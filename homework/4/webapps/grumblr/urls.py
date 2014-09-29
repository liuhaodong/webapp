from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^homepage$', 'grumblr.views.homepage'),
    url(r'^user_stream$','grumblr.views.user_stream'),
    url(r'^user_stream_(?P<id>\d+)$','grumblr.views.specified_user_stream'),
    url(r'^homepage/add_post$','grumblr.views.add_post'),
    url(r'^homepage/delete_post/(?P<id>\d+)$', 'grumblr.views.delete_post'),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'grumblr/login.html'}),
    url(r'^profile$', 'grumblr.views.profile'),
    url(r'^edit_profile$','grumblr.views.edit_profile'),
    url(r'^search_post$','grumblr.views.search_post'),
    url(r'^search_result$','grumblr.views.search_post'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^registration$', 'grumblr.views.registration'),
)
