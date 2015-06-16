from django.conf.urls.defaults import *
import workflow.settings

urlpatterns = patterns('workflow.flow.cclock.lock',
    # Example:
    # (r'^unicenter/', include('unicenter.foo.urls')),

    # Uncomment this for admin:
    #(r'^$', 'views.index'),
    (r'^$', 'views.index'),
)
