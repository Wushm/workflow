# -*- coding: UTF-8 -*-
from django.db import models
from workflow.settings import reviewer1_choices,reviewer2_choices,energy_choices,totaltime_choices,rootcase_choices,leadinto_choices,module_choices,team_choices
from django.contrib import admin

defect_qualifier_choices = (
    (r'Missing', r'Missing'),\
    (r'Incorrect', r'Incorrect'),\
    (r'Extraneous', r'Extraneous'),
)

defect_source_choices = (
    (r'Developed in-house', r'Developed in-house'),\
    #(r'Reused from Library', r'Reused from Library'),\
    #(r'Ported', r'Ported'),\
    #(r'Outsourced', r'Outsourced'),
)

defect_age_choices = (
    (r'Base', r'Base'),\
    (r'New', r'New'),\
    (r'Re-written', r'Re-written'),\
    (r'Re-fixed', r'Re-fixed'),
)
"""
root_cause_choices =  (
    (r'No input', r'No input'),\
    (r'Missing in spec. sheet', r'Missing in spec. sheet'),\
    (r'Wrong description in spec. sheet', r'Wrong description in spec. sheet'),\
    (r'Unclear description in spec. sheet', r'Unclear description in spec. sheet'),\
     
    (r'Description rule violation in spec. sheet', r'Description rule violation in spec. sheet'),\
    (r'Missing modification in spec. sheet', r'Missing modification in spec. sheet'),\
    (r'Mismatch between spec. sheets', r'Mismatch between spec. sheets'),\
    (r'Oversight from spec. sheet', r'Oversight from spec. sheet'),\
    
    (r'Misunderstanding of spec. sheet', r'Misunderstanding of spec. sheet'),\
    (r'Insufficient review of spec. sheet', r'Insufficient review of spec. sheet'),\
    (r'Lack of knowledge on coding', r'Lack of knowledge on coding'),\
    (r'Missing check when reusing', r'Missing check when reusing'),\
    
    (r'Missing check when revising', r'Missing check when revising'),\
    (r'Carelessness', r'Carelessness'),\
    (r'Mis-operation', r'Mis-operation'),\
    (r'Bad communication', r'Bad communication'),\
    
    (r'Standard violation', r'Standard violation'),\
    (r'Wrong review ', r'Wrong review '),\
    (r'Unknown reason', r'Unknown reason'),\
    (r'Others', r'Others'),\
)
"""

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
    DefectTarget = models.CharField(blank=True, null=True, max_length=100)
    DefectType = models.CharField(blank=True, null=True, max_length=100)
    DefectQualifier = models.CharField(blank=True, null=True, max_length=100, choices=defect_qualifier_choices)
    DefectSource = models.CharField(blank=True, null=True, max_length=100, choices=defect_source_choices)
    DefectAge = models.CharField(blank=True, null=True, max_length=100, choices=defect_age_choices)

    
    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

try:
    admin.site.register(Review)
except:
    pass

