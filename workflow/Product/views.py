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

def product_view(request,id):
    prodect = CProduct.objects.get(id=id)
    return render_to_response("product_view.html",\
            {'title':'view product',\
            'product':product,\
            },\
            context_instance=template.RequestContext(request))
