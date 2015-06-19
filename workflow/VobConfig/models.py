# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from workflow.Product.models import CProduct

# Create your models here.
dev_status = (
    (r'',r'---------'),
    (r'dev',r'开发'),
    (r'maintain',r'维护'),      # 维护分支上发现的问题，必须在开发分支上合入。
    (r'close',r'关闭'),         # 关闭的分支，无法合入代码。
)

class CVobConfig(models.Model):
    #标题
    title=models.CharField(max_length=100,verbose_name = u"标题",\
                                      help_text="填写标题，建议与branch name 一致")
    #分支名称
    branch = models.CharField(max_length = 100,verbose_name=u"分支名称",\
                                      help_text="分支branch name , 按照clearcase branch type对应的branch名称填写,请加上后缀@\OnsPlatform")
    #分支开权限服务器
    servers = models.CharField(max_length = 50,verbose_name=u"分支服务器",\
                                      help_text="默认分支服务器为hz_rd_server")
    #分支网页选择名称
    choices = models.CharField(max_length = 100,verbose_name=u'分支网页选择名称',\
                                      help_text="电子流申请时，显示的分支名称,建议与branch name 一致")
    #分支是否有被锁住
    isLock =  models.BooleanField(blank = False,verbose_name="分支锁住状态",\
                                      help_text="如果分支被锁定，就无法提交此分支的电子流")

    #分支的超级管理员，只有此管理员才有权限锁住分支
    superAdmin = models.ForeignKey(User,verbose_name="分支管理员",related_name="CVobConfig_superAdmin",\
                                      help_text="此分支的超级管理员，可以修改分支任何信息")
    #分支开发状态
    devStatus = models.CharField(verbose_name="分支开发状态",max_length=10, choices=dev_status,\
                                      help_text="分支处于不同状态时，电子流申请报表有差异")

    #分支对应的产品,在release tool 的时候需要根据产品进行release
    product = models.ManyToManyField(CProduct,verbose_name = u"产品名称",\
                                      help_text="请选择分支对应的产品名称")
    #分支审核人
    approvers = models.ManyToManyField(User,verbose_name = "审核人",related_name="CVobConfig_approvers",\
                                      help_text="有权利审核电子流的用户")
    #分支主要控制者
    masters = models.ManyToManyField(User,blank = True,null = True,verbose_name = "控制者",related_name='CVobConfig_master',\
                                      help_text="有权利审核电子流,并且始终拥有代码checkin权利")
    #无用字段
    release_number = models.CharField(verbose_name="分支release_numner",max_length=100,null=True,blank=True,\
                                      help_text="暂时无用, 可以考虑不填写")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

try:
    admin.site.register(CVobConfig)
except:
    pass

