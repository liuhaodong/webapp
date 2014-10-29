from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'private_todo_list.views.home'),
    url(r'^add-item', 'private_todo_list.views.add_item'),
    url(r'^delete-item/(?P<id>\d+)$', 'private_todo_list.views.delete_item'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'private-todo-list/login.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login'),
    url(r'^register$', 'private_todo_list.views.register'),
)

