from django.conf.urls.defaults import *

urlpatterns = patterns('workflow.flow.cclock',
    # Example:
    # (r'^unicenter/', include('unicenter.foo.urls')),

    # Uncomment this for admin:
    #(r'^$', 'views.index'),
    (r'^lock/', include('workflow.flow.cclock.lock.urls')),
    (r'^checkmr/', include('workflow.flow.cclock.checkmr.urls')),
    (r'^my/$', 'views.my_cclocks'),
    (r'^my/add/$', 'views.add'),
    (r'^my/newFlow2newMR/$', 'views.newFlow2newMR'),
    (r'^my/(?P<id>\d+)/$', 'views.view'),
    (r'^my/(?P<id>\d+)/rfb_mr/$', 'views.rfb_mr'),
    
    (r'^todo/?q_approve_result=o$', 'views.view_all_approved_result'),
    (r'^todo/$', 'views.todo_cclocks'),
    (r'^todo/(?P<id>\d+)/$', 'views.view'),
    (r'^todo/(?P<id>\d+)/approve/$', 'views.approve'),
    (r'^todo/(?P<id>\d+)/cclock_update/$','views.update'),
    (r'^todo/query','views.query'),
)
