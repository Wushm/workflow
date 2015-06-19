# -*- coding: UTF-8 -*-

from django.conf.urls.defaults import *

from django.contrib import admin

try:
    admin.autodiscover()
except:
    pass

urlpatterns = patterns('workflow.Product',
        (r'^product/(?P<vob_config_id>\d+)/(?P<id>\d+)/$','views.product_view'),
        
)
