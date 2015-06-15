# -*- coding: UTF-8 -*-
from django import forms
from django.forms import ModelForm, Textarea,Select

from workflow.VobConfig.models import CVobConfig
from django.contrib.auth.models import User

class CVobConfigForm(forms.ModelForm):
       def __init__(self,*args,**kwargs):
              super(CVobConfigForm,self).__init__(*args,**kwargs)
              self.fields['approvers'].queryset = User.objects.all().order_by("username")
              self.fields['masters'].queryset = User.objects.all().order_by("username")
              self.fields['superAdmin'].queryset = User.objects.all().order_by("username")
              self.fields['title'].widget.attrs.update({'class': 'vTextField'})
              self.fields['branch'].widget.attrs.update({'class': 'vTextField'})
              self.fields['servers'].widget.attrs.update({'class': 'vTextField'})
              self.fields['choices'].widget.attrs.update({'class': 'vTextField'})
              
              
       class Meta:
              model = CVobConfig
