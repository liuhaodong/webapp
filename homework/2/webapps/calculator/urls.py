from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^hello-world$', 'calculator.views.hello_world'),
    url(r'^hello.html$', 'calculator.views.hello'),
    url(r'^$', 'calculator.views.calculator'),
)

