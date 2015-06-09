# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.Spec.models import SpecIdApplyInfo

class SpecIdForm(forms.ModelForm):
    class Meta:
        model = SpecIdApplyInfo

from workflow.settings import specId_choices

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=40)#提交者工号
    specIdFile = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = specId_choices)
    submitTime_start =forms.DateTimeField(required = False)#提交日期
    submitTime_end =forms.DateTimeField(required = False)#提交日期