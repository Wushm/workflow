# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.NewFile.models import NewFile

class NewFileForm(forms.ModelForm):
    class Meta:
        model = NewFile

branch_choices = (
        (r'NR40K_V1_20070709@\NetRing', r'NR40K_V1_20070709@\NetRing'),\
                (r'feature@\NetRing', r'feature@\NetRing'),\
                (r'NR600V1_BaseV23117@\NetRing', r'NR600V1_BaseV23117@\NetRing'),\
                (r'NR40K_V1_20090204@\NetRing', r'NR40K_V1_20090204@\NetRing'),\
                (r'NR2G5_XC_BOARD@\NetRing', r'NR2G5_XC_BOARD@\NetRing'),\
                (r'2500_Distributed_Final@\NetRing', r'2500_Distributed_Final@\NetRing'),\
                (r'NR10K_BaseV2319SP2@\NetRing', r'NR10K_BaseV2319SP2@\NetRing'),\
                (r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform', r'TN7X5_SBB_V1.2.0_Dev@\OnsPlatform'),\
                (r'TN705_V1.3.2.14_branch@\OnsPlatform', r'TN705_V1.3.2.14_branch@\OnsPlatform'),\
                (r'sbb_V1.3.2.18_base@\OnsPlatform', r'sbb_V1.3.2.18_base@\OnsPlatform'),\
                (r'TN7xx_Universe_Unification_Base@\OnsPlatform', r'TN7xx_Universe_Unification_Base@\OnsPlatform'),\
                (r'TN7xx_V2.2.2.4@\OnsPlatform', r'TN7xx_V2.2.2.4@\OnsPlatform'),\
                (r'TN735_DEV1@\OnsPlatform', r'TN735_DEV1@\OnsPlatform'),\
                (r'TN735_CHT_MAINTIAN@\OnsPlatform', r'TN735_CHT_MAINTIAN@\OnsPlatform'),\
                (r'TN705_V1.5.0.6_maintain@\OnsPlatform', r'TN705_V1.5.0.6_maintain@\OnsPlatform'),\
                (r'test', r'test'),\
                )#分支信息的choice


class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=40)
    mr_id = forms.CharField(max_length = 40)
    vob_branch = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = branch_choices)
