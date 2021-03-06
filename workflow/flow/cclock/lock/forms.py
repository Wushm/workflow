# -*- coding: UTF-8 -*-
from django import forms
from workflow.settings import branch_choices

ACTION_CHOICES=(('q',u'查询'),('assign',u'赋值'),('recover',u'减权'),)

class CCLockForm(forms.Form):
    username = forms.CharField(widget=forms.widgets.TextInput(attrs={'style':'width: 7em;'}), label=u'登录名')
    action = forms.CharField(max_length=3,
                widget=forms.Select(choices=ACTION_CHOICES))
    branch = forms.CharField(max_length=3,
                widget=forms.Select(choices=branch_choices))
