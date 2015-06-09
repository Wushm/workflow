# -*- coding: UTF-8 -*-
from django.db import models
from workflow.settings import newfile_branch_choices
from django.contrib import admin
# Create your models here.

class newfile(models.Model):
    mrs = models.CharField(max_length=60)                                                                    #mr列表            
    vob_branch = models.CharField(max_length=100, choices=newfile_branch_choices)                             #分支
    new_file_list = models.TextField(blank=True, null=True)                                           #新添加文件的全路径名
    link_file_list = models.TextField(blank=True, null=True)                                               #linkto的文件名 
    submitter = models.CharField(max_length=30)                                                       #提交者
    submit_time = models.DateTimeField(blank=True, null=True, auto_now_add = True)                    #请求提交时间
    reserved1 = models.TextField(blank=True, null=True)
    reserved2 = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return ""

    def __unicode__(self):
        return ""

try:
    admin.site.register(newfile)
except:
    pass