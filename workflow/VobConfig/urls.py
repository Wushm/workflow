# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin
try:
    admin.autodiscover()
except:
    pass

urlpatterns = patterns('workflow.VobConfig',
        (r'^add/$','views.add'),
        (r'^all/$','views.all'),
        (r'^view/(?P<id>\d+)/$','views.view'),
        #(r'^refresh/$','views.refresh'),
        #(r'^update/(?P<id>\d+)/$','views.update'),
)
