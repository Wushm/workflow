# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.MrReview.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
    
from workflow.settings import reviewer1_choices, reviewer2_choices, rootcase_choices, module_choices, team_choices

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=40)#提交者工号
    mr_id = forms.CharField(max_length=40)#MR ID
    approver_time =forms.DateTimeField(required = False)#审批日期
    reviewer_one = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = reviewer1_choices)#QM组review人员
    reviewer_two = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = reviewer2_choices)#team leader review人员
    mr_rootcause = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = rootcase_choices)#问题根本原因
    mr_module = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = module_choices)#所属模块或特性
    team_name = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = team_choices)#提交者所属team
    #risk = forms.TextField(blank=False)#风险