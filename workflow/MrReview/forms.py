# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.MrReview.models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
    
from workflow.settings import reviewer1_choices, reviewer2_choices, rootcase_choices, module_choices, team_choices

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=40)#�ύ�߹���
    mr_id = forms.CharField(max_length=40)#MR ID
    approver_time =forms.DateTimeField(required = False)#��������
    reviewer_one = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = reviewer1_choices)#QM��review��Ա
    reviewer_two = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = reviewer2_choices)#team leader review��Ա
    mr_rootcause = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = rootcase_choices)#�������ԭ��
    mr_module = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = module_choices)#����ģ�������
    team_name = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = team_choices)#�ύ������team
    #risk = forms.TextField(blank=False)#����