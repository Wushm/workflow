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
    error_message = ""
    cmd = ''
    count = 1
    ret = 0
    if request.POST:
        version = request.POST['version_number1'] + "." + request.POST['version_number2'] + "." + request.POST['version_number3'] + "." + request.POST['version_number4'] + request.POST['version_number5']
        if HOST_NAME == 'HZ_RD_WUSHUMING' or HOST_NAME == 'HZ_RD_SERVER':
            while(count):
                if action == 'all_release':
                        cmd = r"D:\TN_version\auto_release.bat"+" "+product.product_name+" " + vob_config.title +" "+version+" "+ 'hz_rd_server'
                        ret = os.system(cmd)
                        if (0==ret):
                            message = 'upgrade version no "' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' + 'sucess'
                            request.user.message_set.create(message=message)
                        else:
                            error_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                            break
                        if True == IsVersionReleased(product,branch,version):
                            error_message = '版本已经发布成功，无法再次发布，如果需要再次发布请删除历史数据'
                            break
                        
                        if True == IsVersionReleased(product,branch,version):
                            break
                        cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_note.py " + product.product_name + " " + vob_config.title + " " + version + " " + "resolve"
                        ret = os.system(cmd)
                        if (0==ret):
                            message = 'release_note"' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' + 'resolve MR and generate release notes success!'
                            request.user.message_set.create(message=message)
                        else:
                            error_message = '生成Release note 文件出错'
                            break
                        
                        if True == IsVersionReleased(product,branch,version):
                            break
                        cmd = r"D:\TN_version\upload_ftpserver.bat"+" "+product.product_name
                        ret = os.system(cmd)
                        if (0==ret):
                            message = 'upload_ftpserver "' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' 
                            request.user.message_set.create(message=message)
                        else:
                            error_message = '将文件传输到ftp服务器时出错'
                            break
                        
                        if True == IsVersionReleased(product,branch,version):
                            break
                        cmd = r"python D:\heavysmoker\workspace\suites\suite_version_release\release_mail.py " + product.product_name + " " + vob_config.title + " " + version
                        ret = os.system(cmd)
                        if (0==ret):
                            message = 'release_mail "' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' 
                            request.user.message_set.create(message=message)
                        else:
                            error_message = 'release  mail  失败'
                            break
                        
                        if True == IsVersionReleased(product,branch,version):
                            break
                        cmd = r"D:\TN_version\make_label.bat"+" "+product.prodect_name+" "+ vob_config.title +" "+version+" "+local_server
                        ret = os.system(cmd)
                        if (0==ret):
                            message = 'make_label "' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' 
                            request.user.message_set.create(message=message)
                        else:
                            error_message = 'make_label 失败'
                            break
                        
                elif action == 'update_version':
                    cmd = "D:\TN_version\upgrade_version_no.bat"+" "+ product.product_name +" "+ vob_config.title +" "+ version
                    ret = os.system(cmd)
                    if (0==ret):
                        message = 'upgrade version no "' + 'product:' + product.product_name + 'branch:' + vob_config.title + 'vresion no:' + version + '"' + 'sucess'
                        request.user.message_set.create(message=message)
                        break
                    else:
                        error_message = 'run the cmd:' + '"' + cmd + '"' + 'fail'
                        break
                elif action == 'ready_release':
                    cmd = r"D:\TN_version\auto_release.bat"+" "+product+" "+branch+" "+version+" "+bamboo_server
                    ret = os.system(cmd)	    
                    if (0==ret):
                        html+='product:%s branch:%s get newest version success!'%(product,branch) + r'<br /><br />'
                        break
                    else:
                        html+='product:%s branch:%s get newest version fail!'%(product,branch) + r'<br /><br />'+ 'Please contact admin:QM Team'
                        request.user.message_set.create(message=u"ready_release")
                        break
                count = count - 1
            else:
                error_message = error_message + 'no run web server'
                
            if (ret == 0):
                product.last_release_version = version
                product.save()
       
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
        username = request.GET.get('username', None)
        product = request.GET.get('product', None)
        branch = request.GET.get('branch', None)
        ver_1 = request.GET.get('select_ver_1', None)
        ver_2 = request.GET.get('select_ver_2', None)
        ver_3 = request.GET.get('select_ver_3', None)
        ver_4 = request.GET.get('select_ver_4', None)
        ver_sp = request.GET.get('select_ver_sp', None)
        action = request.GET.get('action', None)
        get_version = request.GET.get('version', None)
        generate_doc = request.GET.get('doc', None)
        upload_server = request.GET.get('server', None)
        send_mail = request.GET.get('mail', None)
        make_lable = request.GET.get('lable', None)
        bamboo_server = request.GET.get('bamboo_server', None)
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
