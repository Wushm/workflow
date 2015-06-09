# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.mr_flow.project_config import project_branch,branch_release_number

from workflow.VobConfig.views import get_branch_choices
from workflow.settings import branch_choices

class  CQNewMRForm(forms.Form):
    cq_username=forms.CharField(max_length=40,widget=forms.widgets.TextInput(\
            attrs={}),label=_(u'username'))#提交者的CQ用户名
    headline = forms.CharField(label=_(u'headline')) #MR对应的headline
    project = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=project_branch, \
            label=_(u'project'))#工程的选择
    vob_branch = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),\
            choices=branch_choices, \
            label=_(u'vob branch'))#发现引起这个MR的分支
    found_release_number = forms.CharField(widget=forms.widgets.TextInput(\
            attrs={}),\
            label=_(u'found release number'))#发现引起这个MR的版本号
    problem_description= forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'problem description'), required=False)
    
    def __init__(self,*args,**kwargs):
        super(CQNewMRForm,self).__init__(*args,**kwargs)
        #修改choices属性
        self.fields['vob_branch'].widget.choices = get_branch_choices()
    

