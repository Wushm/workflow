# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from workflow.settings import branch_choices
from django.contrib import admin
from workflow.VobConfig.views import get_branch_choices

class MR(models.Model):
    mr_id=models.CharField(primary_key=True, max_length=100)#MR ID
    mr_headline=models.CharField(max_length=255, blank=True, null=True)#MR标题
    mr_state=models.CharField(max_length=50, blank=True, null=True)#MR标题

class CCLockFlow(models.Model):
    """
    提交的MR
    审批人直接在数据库里进行配置，不需要保存在数据库
    数据库中只记录最后执行了审批操作的审批人
    primary_approver#主审核人
    sec_approver#第二审核人
    """
    #TODO 必须要有MR查询功能，不然无法
    #提交后就无法修改撤销
    title=models.CharField(max_length=100)#标题
    descn=models.TextField(blank=True)#描述
    bugs = models.ManyToManyField(MR, blank=True, null=True, \
            verbose_name="list of bugs")#bug列表
    vob_branch_1 = models.CharField(max_length=100)#分支
    vob_branch_2 = models.CharField(blank=True, null=True, max_length=100)#分支
    vob_branch_3 = models.CharField(blank=True, null=True, max_length=100)#分支
    vob_branch_4 = models.CharField(blank=True, null=True, max_length=100)#分支
    vob_branch_5 = models.CharField(blank=True, null=True, max_length=100)#分支
    vob_branch_6 = models.CharField(blank=True, null=True, max_length=100)#分支
    who_approver = models.ForeignKey(User, verbose_name="who_approver", blank=True, null=True, \
            related_name="toapp_cclocks")#审批人
    approve_result = models.CharField(max_length=1, blank=True, null=True, \
            choices=(('', u'待审批'), ('o', u'通过'), ('x', u'驳回')))#审核结果
    approve_note = models.TextField(blank=True)#审核时的备注
    submitter = models.ForeignKey(User, verbose_name="submitter", \
            related_name="my_cclocks")#请求提交人
    submit_time = models.DateTimeField(auto_now_add = True)#请求提交时间
    approve_time = models.DateTimeField(null=True, blank=True)#审批时间
    attachments = models.TextField(blank=True)#附件，附件格式 "文件名|原始文件名"
    
    #TODO 增加check code
    approve_check_code = models.CharField(max_length=50, blank=True, null=True)

    def __init__(self,*args,**kwargs):
        super(CCLockFlow,self).__init__(*args,**kwargs)
            
    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

try:
    admin.site.register(MR)
    admin.site.register(CCLockFlow)
except:
    pass
