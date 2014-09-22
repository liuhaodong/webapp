from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^private-todo-list/', include('private_todo_list.urls')),
    url(r'^$', 'private_todo_list.views.home'),
)
