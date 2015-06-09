# -*- coding: UTF-8 -*-
from django.db import models
from workflow.settings import specId_choices,branch_choices
from django.contrib import admin

class SpecIdApplyInfo(models.Model):
    submitter = models.CharField(blank=True, null=True, max_length=30)
    specIdFile = models.CharField(blank=True, null=True, max_length=100, choices=specId_choices)
    maxId = models.IntegerField()
    branch1 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    branch2 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    branch3 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    branch4 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    branch5 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    branch6 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)
    idNumbers = models.CharField(blank=True, null=True, max_length=30)
    submitTime = models.DateField(auto_now_add = True)
    reserved1 = models.TextField(blank=True, null=True)
    reserved2 = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

try:
    admin.site.register(SpecIdApplyInfo)
except:
    pass

