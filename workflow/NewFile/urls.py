#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^blank/(?P<id>\d+)/$', 'workflow.NewFile.views.add_new'),
    (r'^empty_file_query/$', 'workflow.NewFile.views.query_empty_file'),
)
