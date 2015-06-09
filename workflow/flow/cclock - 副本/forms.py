# -*- coding: UTF-8 -*-
from django import forms
from django.utils.translation import gettext as _

from workflow.flow.cclock.models import CCLockFlow
from workflow.VobConfig.views import get_branch_choices

class CCLockFlowForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(CCLockFlowForm,self).__init__(*args,**kwargs)
        
        #修改choices属性
        #self.fields['vob_branch_1'].widget.choices = get_branch_choices()
        #self.fields['vob_branch_2'].widget.choices = get_branch_choices()
        #self.fields['vob_branch_3'].widget.choices = get_branch_choices()
        #self.fields['vob_branch_4'].widget.choices = get_branch_choices()
        #self.fields['vob_branch_5'].widget.choices = get_branch_choices()
        #self.fields['vob_branch_6'].widget.choices = get_branch_choices()
        self.fields['vob_branch_1'].widget = forms.widgets.Select(choices = get_branch_choices())

    class Meta:
        model = CCLockFlow
    
    
INTRODUCTION_PHASE_CHOICE = (
        ('','-------------------',),
        ('HW Electronic Design','HW Electronic Design',),
        ('HW Electronic Design','HW Electronic Design',),
        ('HW Manufacture','HW Manufacture',),
        ('HW Mechanical Design','HW Mechanical Design',),
        ('HW PCB Design','HW PCB Design',),
        ('Process Design','Process Design',),
        ('Process Execution','Process Execution',),
        ('Release','Release',),
        ('Requirement','Requirement',),
        ('S/W Build','S/W Build',),
        ('S/W Configuration','S/W Configuration',),
        ('S/W Design','S/W Design',),
        ('S/W Implementation','S/W Implementation',),
        ('System','System',),
        ('SystemValue','SystemValue',),
        ('USD Writing','USD Writing',),
        )

IMPACTED_UNIT_CHOICE = (
        ('','-------------------',),
        ('Build Script','Build Script',),
        ('Configuration data','Configuration data',),
        ('DD','DD',),
        ('External Release Notes','External Release Notes',),
        ('HLD','HLD',),
        ('HW DD','HW DD',),
        ('Internal Release Notes','Internal Release Notes',),
        ('Load Build Environment','Load Build Environment',),
        ('Make File','Make File',),
        ('Module','Module',),
        ('Process Assets','Process Assets',),
        ('Software Load','Software Load',),
        ('Source Code','Source Code',),
        ('SRS','SRS',),
        ('SystemValue','SystemValue',),
        ('User Document','User Document',),
        )
class RfbMrForm(forms.Form):
    cq_username = forms.CharField(max_length=40, widget=forms.widgets.TextInput(\
        attrs={}), label=_(u'username'))
    cq_password = forms.CharField(max_length=40,\
        widget=forms.widgets.PasswordInput(attrs={}),\
        label=_(u'password'))
    mr_id = forms.CharField(label=_(u'MR ID'))
    reviewer = forms.CharField(label=_(u'Reviewer'), required = False)
    introduction_phase = forms.ChoiceField(widget=forms.widgets.Select(\
        attrs={}), \
        choices = INTRODUCTION_PHASE_CHOICE, \
        label=_(u'Introduction Phase'))
    impacted_unit = forms.ChoiceField(widget=forms.widgets.Select(\
        attrs={}), \
        choices = IMPACTED_UNIT_CHOICE, \
        label=_(u'Impacted Unit'))
    load_information = forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'Load Information'))
    resolutin_by_assignee = forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'Resolutin by Assignee'))
    problem_casued_by_assignee = forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'Problem Casued by Assignee'), required=False)
    files_altered_by_assignee = forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'Files Altered by Assignee'), required=False)
    test_exeCuted_by_assignee = forms.CharField(widget=forms.widgets.Textarea(\
        attrs={}), label=_(u'Test ExeCuted by Assignee'), required=False)


from workflow.settings import branch_choices,approver_choices

class QueryForm(forms.Form):
    submitter_name = forms.CharField(max_length=40)
    approver_name =forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = approver_choices)
    mr_id = forms.CharField(max_length = 40)
    vob_branch = forms.ChoiceField(widget=forms.widgets.Select(attrs={}),choices = branch_choices)
