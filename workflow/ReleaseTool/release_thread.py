# -*- coding: UTF-8 -*-
#!/usr/bin/env python
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from workflow.settings import HOST_NAME
from workflow.Product.models import CProduct

import threading, time
import os
import re


threadQueue={}
release_history = r"D:\TN_version\release_history.txt"

def IsVersionReleased(product,branch,version):
    line_list = open(release_history,'a+')
    for line in line_list:
        if None!=re.search(product+' '+branch+' '+version, line):            
            line_list.close()
            return True    
    return False

def record_version(product,branch,version):
    line_list = open(release_history,'a+')    
    line_list.write(product+' '+branch+' '+version+'\n')
    line_list.close()


class releaseThread( threading.Thread ):
    product = None
    branch = None
    version = None
    server = 'hz_rd_server'
    get_version = True
    generate_doc = True
    upload_server = True
    send_mail = True
    make_lable = True
    err_message = None  
    message = None
    release_result = None
    action = None
    product_id = 0
    def __init__( self,action,product,branch,version,product_id):
        super( releaseThread, self ).__init__()
        self.name = product + '_release_tool'
        self.action = action
        self.product = product
        self.branch = branch
        self.version = version
        self.product_id = product_id
        
    def setOption(self,get_version = True,generate_doc = True,upload_server = True,send_mail = True,make_lable = True):
        self.get_version = get_version
        self.generate_doc = generate_doc
        self.upload_server = upload_server
        self.send_mail = send_mail
        slef.make_lable = make_lable
       
    def ready_release(self):
        ret = 0
        if HOST_NAME == 'HZ_RD_SERVER':
            if True == IsVersionReleased(self.product,self.branch,self.version):
                    slef.err_message = '版本已经发布成功，无法再次发布，如果需要再次发布请删除//hz_rd_server/TN_version/release_history.txt里面历史版本号'
                    return False
    
        cmd = r"D:\TN_version\auto_release.bat"+" "+ self.product+" " + self.branch  +" "+ self.version +" "+ self.server
        self.message = "正在预发布版本，请稍后刷新..."
        if HOST_NAME == 'HZ_RD_SERVER':
            ret = os.system(cmd)
        else:
            time.sleep(3)

        if (0==ret):
            self.message = 'get_version"' + 'product:' + self.product + '  branch:' + self.branch  + '   vresion no:' + self.version + '"' + 'sucess'
        else:
            self.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
            return -1
        return ret
    
    def update_version(self):
        ret = 0
        cmd = "D:\TN_version\upgrade_version_no.bat"+" "+ self.product + " " + self.branch  + " " + self.version
        self.message = "正在更新版本号，请耐心等待..."
        if HOST_NAME == 'HZ_RD_SERVER':
            ret = os.system(cmd)
        else:
            time.sleep(3)
        if (0==ret):
            self.message = 'update_version"' + 'product:' + self.product + '  branch:' + self.branch  + '   vresion no:' + self.version + '"' + 'sucess'
        else:
            elf.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
            return -1
        return ret
    
    def all_release(self):
        ret = 0
        if(self.get_version):
            ret = self.ready_release()
            if(ret is not 0):
                return -1
        if(self.generate_doc):
            time.sleep(2)
            cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_note.py " + self.product + " " + self.branch  + " " + self.version + " " + "resolve"
            self.message = "正在获取resolve MR，请耐心等待..."
            if HOST_NAME == 'HZ_RD_SERVER':
                ret = os.system(cmd)
            else:
                time.sleep(2)
      
            if(ret == 0):
                self.message = 'release_note"' + 'product:' + self.product+ ' branch:' + self.branch  + 'vresion no:' + self.version + '"' + 'resolve MR and generate release notes success!'
            else:
                self.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                return -1
        
        if(self.upload_server):
            time.sleep(2)
            cmd = r"D:\TN_version\upload_ftpserver.bat"+" "+self.product
            self.message = "正在将文件上传到FTP服务器，请内心等待..."
            if HOST_NAME == 'HZ_RD_SERVER':
                ret = os.system(cmd)
            else:
                time.sleep(2)
           
            if(ret == 0):
                self.message = 'upload_ftpserver"' + 'product:' + self.product+ ' branch:' + self.branch  + 'vresion no:' + self.version + '"' + 'success!'
            else:
                self.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                return -1
            
        if(self.send_mail):
            time.sleep(2)
            cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_mail.py " + self.product + " " + self.branch  + " " + self.version
            self.message = "正在发送邮件，请内心等待..."
            if HOST_NAME == 'HZ_RD_SERVER':
                ret = os.system(cmd)
            else:
                time.sleep(2)
    
            if(ret == 0):
                self.message = 'send_mail"' + 'product:' + self.product+ ' branch:' + self.branch  + 'vresion no:' + self.version + '"' + 'success!'
            else:
                self.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                return -1
        
        if(self.make_lable):
            time.sleep(2)
            cmd = r"D:\TN_version\make_label.bat"+" "+self.product + " " + self.branch  + " " + self.version+" "+ 'hz_rd_server'
            self.message = "正在打标签，请内心等待..."
            if HOST_NAME == 'HZ_RD_SERVER':
                ret = os.system(cmd)
            else:
                time.sleep(2)
  
            if(ret == 0):
                self.message = 'make_lable"' + 'product:' + self.product+ ' branch:' + self.branch  + 'vresion no:' + self.version + '"' + 'success!'
            else:
                self.err_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                return -1
        if(ret == 0 ):
            if HOST_NAME == 'HZ_RD_SERVER':
                product = CProduct.objects.get(id=self.product_id)
                product.last_release_version = self.version
                product.save()
            
        return ret
    
    def run( self ):
        ret = 0
        print "starting====", self.name, time.ctime()
        print(self.product,self.branch,self.version)
        
        self.message = "start run thread " +'time: "' + time.ctime() + '"' + ' product:' + self.product + ' branch:' + self.branch + ' version:' + self.version 
        time.sleep(5)
        
        if self.action == 'all_release':
            ret = self.all_release()
            if(ret is not 0):
                release_result = 'fail'
                return 
          
        if self.action == 'ready_release':
            ret = self.ready_release()
            if(ret is not 0):
                release_result = 'fail'
                return 
        
        if self.action == 'update_version':
            ret = self.update_version()
            if(ret is not 0):
                release_result = 'fail'
                return 
        
        self.release_result = 'succes'
        
        self.message = 'end run thread ' +'time: "' + time.ctime() + '"' + ' product:' + self.product + ' branch:' + self.branch + ' version:' + self.version + ' release succes'
        print(self.release_result,self.message,self.err_message)


