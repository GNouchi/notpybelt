from django.conf.urls import url
from . import views
urlpatterns  = [
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
    url(r'^wall$', views.wall),
    url(r'^$', views.index),
    url(r'^addjob$', views.addjob),
    url(r'^createjob$', views.createjob),
    url(r'^show/(?P<id>\d)$', views.show),
    url(r'^edit/(?P<id>\d)$', views.edit),
    url(r'^editjob/(?P<id>\d)$', views.editjob),
    url(r'^takejob/(?P<id>\d)$', views.takejob),   
    url(r'^destroy/(?P<id>\d)$', views.destroy),   
]