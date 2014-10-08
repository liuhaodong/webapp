from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^shared-todo-list/', include('shared_todo_list.urls')),
)
