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

def product_view(request,vob_config_id,id):
    product = CProduct.objects.get(id=id)
    vob_config =CVobConfig.objects.get(id=vob_config_id)
    can_release = True
    #if product.product_manager.id == request.user.id:
        #can_release = True
    return render_to_response("product_view.html",\
            {'title':'view product',\
            'product':product,\
            'vob_config':vob_config,\
            'can_release':can_release,\
            },\
            context_instance=template.RequestContext(request))
