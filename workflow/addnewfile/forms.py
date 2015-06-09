# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.addnewfile.models import newfile
from workflow.settings import newfile_branch_choices

class NewFileForm(forms.ModelForm):
    class Meta:
        model = newfile

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=30)
    mr_id = forms.CharField(max_length = 60)
    vob_branch = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = newfile_branch_choices)
    filename = forms.CharField(max_length=40)
    submitTime_start =forms.DateTimeField(required = False)
    submitTime_end =forms.DateTimeField(required = False)
