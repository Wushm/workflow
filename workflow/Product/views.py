# -*- coding: UTF-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from workflow.VobConfig.models import CVobConfig
from workflow.Product.models import CProduct

from workflow.ReleaseTool.release_thread import releaseThread,threadQueue
def product_view(request,vob_config_id,id):
    product = CProduct.objects.get(id=id)
    vob_config =CVobConfig.objects.get(id=vob_config_id)
    can_release = True
    #if product.product_manager.id == request.user.id:
        #can_release = True
    thread = threadQueue.get(product.product_name,None)
    err_message = None
    if(thread is not None):
        if(thread.isAlive()):
            request.user.message_set.create(message=thread.message)
            can_release = False
        else:
            if (thread.release_result == 'succes'):
                request.user.message_set.create(message=thread.message)
            else:
                err_message = thread.err_message
            del(threadQueue[product.product_name])
            can_release = True
    
    return render_to_response("product_view.html",\
            {'title':'view product',\
            'product':product,\
            'vob_config':vob_config,\
            'can_release':can_release,\
            'error_message':err_message,\
            },\
            context_instance=template.RequestContext(request))
