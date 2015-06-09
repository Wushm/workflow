from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Example:
    # (r'^unicenter/', include('unicenter.foo.urls')),

    # Uncomment this for admin:
    (r'^$', 'workflow.portal.views.index'),
    (r'^login/$', 'workflow.portal.views.login'),
    (r'^t_list/$', 'workflow.portal.views.t_list'),    
    (r'^t_edit/$', 'workflow.portal.views.t_edit'),    
    ('^logout/$', 'django.contrib.auth.views.logout'),    
    ('^password_change/$', 'django.contrib.auth.views.password_change'),        
)
