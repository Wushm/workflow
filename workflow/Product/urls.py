# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin

try:
    admin.autodiscover()
except:
    pass

urlpatterns = patterns('workflow.Product',
        (r'^(?P<id>\d+)/product/$','views.product_view'),
        
)
