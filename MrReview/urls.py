# -*- coding: UTF-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('workflow.MrReview',
    (r'^todo/query','views.query'),
    (r'^add/(?P<id>\d+)/$','views.add'),
    (r'^view/(?P<id>\d+)/$', 'views.view'),
    (r'^update/(?P<id>\d+)/$','views.update'),
)