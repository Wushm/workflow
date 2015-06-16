from django.conf.urls.defaults import *
import workflow.settings

urlpatterns = patterns('workflow.mr_flow',
    # Example:
    # (r'^unicenter/', include('unicenter.foo.urls')),

    # Uncomment this for admin:
    #(r'^$', 'views.index'),
    (r'^$', 'views.index'),
    (r'^edit','views.edit'),
    (r'^query','views.query'),
)
