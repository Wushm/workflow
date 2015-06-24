# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# Create your models here.
class CProduct(models.Model):
    #标题
    title=models.CharField(max_length=100,verbose_name = u"标题",\
                                      help_text="填写标题，建议product name 加上对应的市场")
    product_name = models.CharField(max_length=100,verbose_name = u"产品名称",\
                                      help_text="填写对应的产品,例如'TN703a'")
    last_release_version = models.CharField(verbose_name="最后的release版本",max_length=100,\
                                      help_text="第一次生成时，通过cc系统确认") 
    #分支的超级管理员，只有此管理员才有权限锁住分支
    product_manager= models.ForeignKey(User,verbose_name="产品管理员",related_name="product manager",\
                                      help_text="此产品的管理员，产品发布版本有此管理员负责")
    
    product_branch = models.CharField(max_length=100,verbose_name = u"产品branch",\
                                      help_text="产品release对应的branch名称")

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

try:
    admin.site.register(CProduct)
except:
    pass

