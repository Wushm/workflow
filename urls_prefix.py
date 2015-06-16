#!/usr/bin/env python
# coding: utf-8
from django.conf.urls.defaults import *
from workflow.settings import *

urlpatterns = patterns('',
    # Example:
    # (r'^unicenter/', include('unicenter.foo.urls')),

    # Uncomment this for admin:
    #(r'^', include('urls')),    
    (r'^%s/' % URL_PREFIX, include('workflow.urls')),    
)
