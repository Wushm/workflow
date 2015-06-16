# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('workflow.Spec',
    (r'^add/$','views.add'),
    (r'^todo/query/$','views.query'),
)