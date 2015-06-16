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
        (r'^refresh/$','views.refresh'),
        (r'^update/(?P<id>\d+)/$','views.update'),
        (r'^lock/(?P<id>\d+)/$','views.lock'),
)
