# -*- coding: UTF-8 -*-
#from django import newforms as forms
from django import forms

STATES_CHOICES = (\
        ('', 'ALL'),\
        ('ReadyForBuild', 'ReadyForBuild'),\
        ('Resolved', 'Resolved'),\
        )

class SearchMRForm(forms.Form):
    """
    查询MR
    """
    start_date = forms.DateField(widget=forms.widgets.TextInput(attrs={'class':'vDateField'}))
    end_date = forms.DateField(widget=forms.widgets.TextInput(attrs={'class':'vDateField'}))
    state = forms.CharField(max_length=3,
                widget=forms.Select(choices=STATES_CHOICES))    

class UpdateMRForm(forms.Form):
    """
    更新MR
    """
    cq_username = forms.CharField(max_length=40,\
            #widget=forms.widgets.TextInput(attrs={'style':'width: 20em;'}),\
            label='Clear Quest用户名', required=False)
    cq_pswd = forms.CharField(max_length=40,\
            widget=forms.widgets.PasswordInput(),\
            label='Clear Quest密码', required=False)
