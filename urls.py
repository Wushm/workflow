from django.conf.urls.defaults import *
from workflow import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
try:
    admin.autodiscover()
except:
    pass

urlpatterns = patterns('',
    # Example:
    # (r'^cclock/', include('cclock.foo.urls')),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    #(r'^static/(?P<path>.*)$', 'django.views.static.serve',
    #    {'document_root': settings.MEDIA_ROOT}),    
    (r'^admin/(.*)', admin.site.root),
    (r'^mr_flow/',include('workflow.mr_flow.urls')),
    (r'^cclock/', include('workflow.flow.cclock.urls')),
    (r'^mr_review/', include('workflow.MrReview.urls')),
    (r'^spec/', include('workflow.Spec.urls')),
    (r'^', include('workflow.portal.urls')),
    (r'^newfile/', include('workflow.addnewfile.urls')),
    (r'^vob_config/',include('workflow.VobConfig.urls')),
)
