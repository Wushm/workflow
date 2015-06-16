# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
dev_status = (
    (r'',r'---------'),
    (r'dev',r'开发'),
    (r'maintain',r'维护'),
    (r'close',r'关闭'),
)

class CVobConfig(models.Model):
    title=models.CharField(max_length=100,verbose_name = u"标题")#标题
    #分支名称
    branch = models.CharField(max_length = 100,verbose_name=u"分支名称") 
    #分支开权限服务器
    servers = models.CharField(max_length = 50,verbose_name=u"分支服务器")
    #分支网页选择名称
    choices = models.CharField(max_length = 100,verbose_name=u'分支网页选择名称') 
    #分支审核人
    approvers = models.ManyToManyField(User,verbose_name = "审核人",related_name="CVobConfig_approvers")
    #分支主要控制者
    masters = models.ManyToManyField(User,blank = True,null = True,verbose_name = "控制者",related_name='CVobConfig_master')
    #分支是否有被锁住
    isLock =  models.BooleanField(blank = False,verbose_name="分支锁住状态")
    #分支的超级管理员，只有此管理员才有权限锁住分支
    superAdmin = models.ForeignKey(User,verbose_name="分支管理员",related_name="CVobConfig_superAdmin")
    #分支开发状态
    devStatus = models.CharField(verbose_name="分支开发状态",max_length=10, choices=dev_status)
    #分支release_number
    release_number = models.CharField(verbose_name="分支release_number",max_length=10, \
                                      help_text="分支release_numbe,可以通过CQ系统查询,一般性特指最后一个版本号")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

try:
    admin.site.register(CVobConfig)
except:
    pass

