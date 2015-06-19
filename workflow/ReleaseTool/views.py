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

def release(request,vob_config_id,id):
    vob_config =CVobConfig.objects.get(id=vob_config_id)
    product = CProduct.objects.get(id=id)
    action = request.GET.get('action')
    print(action)
    return render_to_response("release.html",\
            {'title':'release version',\
            },\
            context_instance=template.RequestContext(request))
    

