# -*- coding: UTF-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from workflow.VobConfig.models import CVobConfig
from workflow.Product.models import CProduct
from workflow.ReleaseTool.form import CReleasToolForm
from workflow.settings import HOST_NAME
import os
import re
from workflow.ReleaseTool.release_thread import releaseThread,threadQueue

def release(request,vob_config_id,id):
    vob_config =CVobConfig.objects.get(id=vob_config_id)
    product = CProduct.objects.get(id=id)
    releaseForm = CReleasToolForm()
    action = request.GET.get('action')
    
    button_view = '';
    if action == 'all_release':
        button_view = '完整发布'
    elif action == 'ready_release':
        button_view = '预发布'
    elif action == 'update_version':
        button_view = '更新版本号'
    releaseForm.init_version_choices(product.last_release_version)
    error_message = None
    cmd = ''
    count = 1
    ret = 0
    if request.POST:
        version = request.POST['version_number1'] + "." + request.POST['version_number2'] + "." + request.POST['version_number3'] + "." + request.POST['version_number4'] + request.POST['version_number5']
        thread = threadQueue.get(product.product_name,None)
        #根据队列里面任务，创建任务或者返回任务运行情况
        if(thread is not None):
            if(thread.isAlive()):
                request.user.message_set.create(message=thread.message)
            else:
                if (thread.release_result == 'succes'):
                    request.user.message_set.create(message=thread.message)
                else:
                    error_message = thread.err_message
                    del(threadQueue[product.product_name])
        else:
            thread = releaseThread(action,product.product_name,product.product_branch,version,id)
            threadQueue[product.product_name] = thread
            thread.start()
        redirect_to = '../../../../product_manage/product/' + vob_config_id  + '/' + id + '/'
        return HttpResponseRedirect(redirect_to)    
 
    return render_to_response("release.html",\
            {'title':'release version',\
            'product':product,\
            'vob_config':vob_config,\
            'action':action,\
            'button_view':button_view,\
            'releaseForm':releaseForm,\
            'error_message': error_message,\
            },\
            context_instance=template.RequestContext(request))

    
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

def release_old(request):
    if request.POST:
        username = request.user.first_name
        product = request.POST['product']
        branch = request.POST['branch']
        ver_1 = request.POST['select_ver_1']
        ver_2 = request.POST['select_ver_2']
        ver_3 = request.POST['select_ver_3']
        ver_4 = request.POST['select_ver_4']
        ver_sp = request.POST['select_ver_sp']
        action = request.POST['action']
        get_version = request.POST['version']
        generate_doc = request.POST['doc']
        upload_server = request.POST['server']
        send_mail = request.POST['mail']
        make_lable = request.POST['lable']
        bamboo_server = request.POST['bamboo_server']
        local_server = os.getenv('computername').lower()
        print "bamboo_server is " + bamboo_server
        print "local server is " + local_server
            
        if(ver_sp == None):
            version = ver_1 + "." + ver_2 + "." + ver_3 + "." + ver_4 
        else:
            version = ver_1 + "." + ver_2 + "." + ver_3 + "." + ver_4 + ver_sp
            
        html=''
        if "update version id" == action:
            if "3160" == product:
                cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\c3160_prepare.py " + version + " prepare"
            elif "onu"==product:
                if "onu204i_k7"==branch:
                    cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\linux_update_version_no.py"+" "+product+" "+branch+" "+version
            else:
                cmd = "D:\TN_version\upgrade_version_no.bat"+" "+product+" "+branch+" "+version
                    
            ret = os.system(cmd)
            if (0==ret):
                html='product:%s branch:%s update to version No.:%s success!'%(product,branch,version) + r'<br />'
            else:
                html='product:%s branch:%s update to version No.:%s fail! The clearcase view maybe is updating, so can not do check out and check in now'%(product,branch,version) + r'<br />'
                    
            return HttpResponse(html)
        elif "get pre-release version" == action:
            cmd = r"D:\TN_version\auto_release.bat"+" "+product+" "+branch+" "+version+" "+bamboo_server
            ret = os.system(cmd)	    
            if (0==ret):
                html+='product:%s branch:%s get newest version success!'%(product,branch) + r'<br /><br />'
            else:
                html+='product:%s branch:%s get newest version fail!'%(product,branch) + r'<br /><br />'+ 'Please contact admin:QM Team'
                return HttpResponse(html)
            
            if product != "netring":
                cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_note.py " + product + " " + branch + " " + version + " " + "RFB"
                ret = os.system(cmd)
                if (0==ret):		
                    html+='product:%s branch:%s version:%s RFB MR and generate release notes success!'%(product,branch,version) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s version:%s RFB MR and generate release notes fail!'%(product,branch,version) + r'<br /><br />'+ 'Please contact admin:QM Team'  
                
            return HttpResponse(html)    	
        else:
            #generate_doc,upload_server,make_lable need check released version while get_version,send_mail needn't.
            #The reason is that:generate_doc,upload_server,make_lable can't revert.
            if get_version:
                cmd = r"D:\TN_version\auto_release.bat"+" "+product+" "+branch+" "+version+" "+bamboo_server
                ret = os.system(cmd)	    
                if (0==ret):
                    html+='product:%s branch:%s get newest version success!'%(product,branch) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s get newest version fail!'%(product,branch) + r'<br /><br />'+ 'Please contact admin:QM Team'
                    return HttpResponse(html)
            
            if generate_doc:
                if True == IsVersionReleased(product,branch,version):
                    return HttpResponse('The product:%s branch:%s version:%s have already released.<br>\
                        <br>\
                        You can release a newer version or contact admin:QM Team'%(product,branch,version))
    
                cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_note.py " + product + " " + branch + " " + version + " " + "resolve"
                ret = os.system(cmd)
                if (0==ret):		
                    html+='product:%s branch:%s version:%s resolve MR and generate release notes success!'%(product,branch,version) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s version:%s resolve MR and generate release notes fail!'%(product,branch,version) + r'<br /><br />'+ 'Please contact admin:QM Team'
                    return HttpResponse(html)
                
            if upload_server:
                if True == IsVersionReleased(product,branch,version):
                    return HttpResponse('The product:%s branch:%s version:%s have already released.<br>\
                        <br>\
                        You can release a newer version or contact admin:QM Team'%(product,branch,version))
                
                cmd = r"D:\TN_version\upload_ftpserver.bat"+" "+product
                ret = os.system(cmd)
                if (0==ret):
                    html+='product:%s branch:%s version:%s upload to server success!'%(product,branch,version) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s version:%s upload to server fail!'%(product,branch,version) + r'<br /><br />'+ 'Please contact admin:QM Team'
                    return HttpResponse(html)
                
            if send_mail:
                if True == IsVersionReleased(product,branch,version):
                    return HttpResponse('The product:%s branch:%s version:%s have already released.<br>\
                        <br>\
                        You can release a newer version or contact admin:QM Team'%(product,branch,version))
                        
                cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_mail.py " + product + " " + branch + " " + version
                ret = os.system(cmd)
                if (0==ret):
                    html+='product:%s branch:%s version:%s send release mail success!'%(product,branch,version) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s version:%s send release mail fail!'%(product,branch,version) + r'<br /><br />'+ 'Please contact admin:QM Team'
                    return HttpResponse(html)
                    
            #record version.
            #record_version(product,branch,version)
            
            if make_lable:
                if True == IsVersionReleased(product,branch,version):
                    return HttpResponse('The product:%s branch:%s version:%s have already released.<br>\
                        <br>\
                        You can release a newer version or contact admin:QM Team'%(product,branch,version))
                    
                cmd = r"D:\TN_version\make_label.bat"+" "+product+" "+branch+" "+version+" "+local_server
                ret = os.system(cmd)
                if (0==ret):
                    html+='product:%s branch:%s version:%s will make lable at once!'%(product,branch,version) + r'<br /><br />'
                else:
                    html+='product:%s branch:%s version:%s make lable fail!'%(product,branch,version) + r'<br /><br />'+ 'Please contact admin:QM Team'
                    return HttpResponse(html)
                
            #record version.
            record_version(product,branch,version)
                
            return HttpResponse(html)
    else:
        return render_to_response("release_old.html",\
            {'title':'old release version'},\
            context_instance=template.RequestContext(request))
