# -*- coding: UTF-8 -*-
from django.db import models
from workflow.settings import branch_choices
from django.contrib import admin
# Create your models here.

class NewFile(models.Model):
    mrs = models.TextField()                                                                            #mr列表            
    vob_branch_1 = models.CharField(max_length=100, choices=branch_choices)                             #分支1
    vob_branch_2 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)      #分支2
    vob_branch_3 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)      #分支3
    vob_branch_4 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)      #分支4
    vob_branch_5 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)      #分支5
    vob_branch_6 = models.CharField(blank=True, null=True, max_length=100, choices=branch_choices)      #分支6
    file_full_name = models.TextField()                                                                 #新添加文件的全路径名
    submitter = models.CharField(max_length=30)                                                         #提交者
    approver = models.CharField(blank=True, null=True, max_length=30)                                   #审批者
    submit_time = models.DateTimeField(blank=True, null=True, auto_now_add = True)                      #请求提交时间
    
    
    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

try:
    admin.site.register(NewFile)
except:
    pass