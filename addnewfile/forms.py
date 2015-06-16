# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.addnewfile.models import newfile
from workflow.settings import newfile_branch_choices
from workflow.VobConfig.views import get_branch_choices

class NewFileForm(forms.ModelForm):
    class Meta:
        model = newfile
    def __init__(self,*args,**kwargs):
        super(NewFileForm,self).__init__(*args,**kwargs)
        self.fields['vob_branch'].widget.choices = get_branch_choices()

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=30)
    mr_id = forms.CharField(max_length = 60)
    vob_branch = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = newfile_branch_choices)
    filename = forms.CharField(max_length=40)
    submitTime_start =forms.DateTimeField(required = False)
    submitTime_end =forms.DateTimeField(required = False)

    def __init__(self,*args,**kwargs):
        super(QueryForm,self).__init__(*args,**kwargs)
        self.fields['vob_branch'].widget.choices = get_branch_choices()
