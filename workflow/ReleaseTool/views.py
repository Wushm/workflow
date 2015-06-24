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
    error_message = ""
    cmd = ''
    count = 1
    ret = 0
    if request.POST:
        version = request.POST['version_number1'] + "." + request.POST['version_number2'] + "." + request.POST['version_number3'] + "." + request.POST['version_number4'] + request.POST['version_number5']
        if HOST_NAME == 'HZ_RD_WUSHUMING':
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
                
       
    return render_to_response("release.html",\
            {'title':'release version',\
            'product':product,\
            'vob_config':vob_config,\
            'action':action,\
            'releaseForm':releaseForm,\
            'error_message': error_message,\
            },\
            context_instance=template.RequestContext(request))
    

