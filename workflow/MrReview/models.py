# -*- coding: UTF-8 -*-
from django.db import models
from workflow.settings import reviewer1_choices,reviewer2_choices,energy_choices,totaltime_choices,rootcase_choices,leadinto_choices,module_choices,team_choices
from django.contrib import admin

class Review(models.Model):
    workflow_id = models.IntegerField()
    mrs = models.TextField(blank=True, null=True)#mr列表
    submitter = models.CharField(blank=True, null=True, max_length=30)#submitter
    reviewer1 = models.CharField(blank=True, null=True, max_length=100, choices=reviewer1_choices)#reviewer1
    reviewer2 = models.CharField(blank=True, null=True, max_length=100, choices=reviewer2_choices)# reviewer2
    reviewer3 = models.CharField(blank=True, null=True, max_length=100, choices=reviewer2_choices)# reviewer3
    reviewer2_energy = models.CharField(blank=True, null=True, max_length=100, choices=energy_choices)#review2投入度
    reviewer3_energy = models.CharField(blank=True, null=True, max_length=100, choices=energy_choices)#review3投入度
    totalTime = models.CharField(blank=True, null=True, max_length=100, choices=totaltime_choices)#review时间
    mrRootCause = models.CharField(blank=True, null=True, max_length=100, choices=rootcase_choices)#mr原因
    isLeadInto = models.CharField(blank=True, null=True, max_length=100, choices=leadinto_choices)#是否是引入
    module = models.CharField(blank=True, null=True, max_length=100, choices=module_choices)#模块或特性
    team = models.CharField(blank=True, null=True, max_length=100, choices=team_choices)#team
    reasonDecription = models.TextField(blank=True, null=True)#问题原因描述
    risk = models.TextField(blank=True, null=True)#风险
    typicalQuestion = models.TextField(blank=True, null=True)#典型问题
    questionNum = models.CharField(blank=True, null=True, max_length=100)#发现问题个数
    questionDecr = models.TextField(blank=True, null=True)#发现问题描述
    reviewTime = models.DateField(auto_now_add = True)#mr review时间
    reserved1 = models.TextField(blank=True, null=True)
    reserved2 = models.TextField(blank=True, null=True)
    reserved3 = models.TextField(blank=True, null=True)
    reserved4 = models.TextField(blank=True, null=True)
    reserved5 = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

try:
    admin.site.register(Review)
except:
    pass

