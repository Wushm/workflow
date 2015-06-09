#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^add/$', 'workflow.addnewfile.views.add'),
    (r'^query/$', 'workflow.addnewfile.views.query'),
)
