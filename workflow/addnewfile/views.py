# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Q

from workflow.addnewfile.models import newfile
from workflow.addnewfile.forms import NewFileForm, QueryForm
from workflow.settings import jobnumber_name
import re

import os
from subprocess import *
import tempfile

#bat file in hz_rd_build3
bat_file = r'c:\heavysmoker\workspace\suites\suite_version_release\workflow_addnew.bat'
server_cc_dir = r"\\hz_rd_build3\ClearCase"

branch_dic = {
    "TN735_DEV1"                       : r"rsh_735\OnsPlatform",
    "TN7xx_Universe_Unification_Base"  : r"rsh_uni\OnsPlatform",
    "TN7X5_SBB_V1.2.0_Dev"             : r"rsh_sbb_1_2_0\OnsPlatform",
    "TN705_V1.3.2.14_branch"           : r"rsh_765\OnsPlatform",
    "TN7xx_V2.2.2.4"                   : r"rsh_uni_2_2\OnsPlatform",
    "TN705_V1.5.0.6_maintain"          : r"rsh_sbb_705\OnsPlatform",
    "TN7xx_V2.2.3.x"                   : r'rsh_uni_2_2_3\OnsPlatform',
    "TN705_SBB_Private_svcoam"         : r'rsh_sbb_705_svcoam\OnsPlatform',
    "725E_dev"                         : r'rsh_725E\OnsPlatform',
}

#define log
def initlog():
    import logging
    logger = logging.getLogger('addnewfile')
    hdlr = logging.FileHandler(r'E:\addnewfile.log')
    formatter = logging.Formatter('[%(asctime)s]%(name)-12s:%(levelname)-8s"%(message)s"')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    
    return [logger,hdlr]

def log_Msg(message):
    newfile_logger,hdlr = initlog()
    newfile_logger.debug(message)
    hdlr.flush()
    newfile_logger.removeHandler(hdlr)
    hdlr.flush()
    hdlr.close()

def copyfile():
    src = file(os.path.join(tempfile.gettempdir(), 'cc_temp.txt'), "r+")
    des = open(r"E:\addnewfile.log", "a")
    des.writelines(src.read())
    src.close()
    des.close()

def cc_action(cc_dir, new_file, link):
    #link num
    if cmp(link,'') != 0:
        link_list = link.split(',')
        link_len = len(link_list)
    else:
        link_len =0
        
    #whether file or dir
    isfile = "False"
    tmp_list = new_file.split('.')
    if len(tmp_list) > 1:
        isfile = "True"
    
    
    command_line = 'onsrsh.exe hz_rd_build3 cmd.exe /c call '+' '+bat_file+ ' '+ cc_dir + ' ' + new_file
    command_add = command_line + '  True'+ ' ' +isfile+ ' ' + str(link_len) + ' ' + '"'+ link +'"'
        
    #print command_add
    args = command_add.split(' ')
    log_Msg("args:" + str(args))

    #print os.path.join(tempfile.gettempdir(), 'cc_temp.txt')
    xfile = file(os.path.join(tempfile.gettempdir(), 'cc_temp.txt'), 'w+')

    p1 = Popen(args,stdout=xfile)
    p1.wait()
    xfile.close()
    if p1.returncode != 0:  
        log_Msg("Popen Error.")
        return 1

    xfile = file(xfile.name)
    cc_str = xfile.read().decode("mbcs").splitlines()
    xfile.close()
    #print cc_str
    cc_err = 0
    for i in range(len(cc_str)) :
        if cc_str[i].find('cleartool: Error:') > -1 : # fail
            log_Msg("cleartool Error")
            cc_err = 1
            
    if cc_err:
        command_del = command_line + " False"
        args = command_add.split(' ')
        log_Msg("cc_err--args:" + str(args))
        xfile = file(os.path.join(tempfile.gettempdir(), 'cc_temp.txt'), 'a+')
    
        p1 = Popen(args,stdout=xfile)
        p1.wait()
        xfile.close()
        if p1.returncode != 0:  
            log_Msg("Popen Error.")
        
        return 2

    return 0
 

def add(request):
    if jobnumber_name.has_key(str(request.user)):
        submitter = jobnumber_name[str(request.user)][0]
    else:
        submitter = request.user
        
    data = {}
    data['submitter'] = submitter

    form = NewFileForm(data)
    
    if request.POST:
        data = request.POST.copy()
        newfile_list = data['new_file_list']
        linkfile_list = data['link_file_list']

        log_Msg("newfile_list:" + str(newfile_list))
        log_Msg("linkfile_list:" + str(linkfile_list))
        
        newfiles_dir = {}
        files = newfile_list.split(";")
        links = linkfile_list.split(';')
        branch = data['vob_branch'][: len(data['vob_branch'])-13]
        
        #find cc branch
        find_branch = 0
        for key in branch_dic.keys():
            if cmp(key, branch) == 0:
                cc_branch = branch_dic[key]
                find_branch = 1
                break
            
        if find_branch == 0:
            return HttpResponse("hz_rd_build3上不存在该分支，不能添加！")
        
        for i in range(0, len(files)):
            if(files[i] != ""):
                
                #判断新加文件或者目录所在的文件夹是否存在
                fullname = server_cc_dir +'\\' + branch_dic[branch] + '\\' + files[i]
                #print fullname
                if(os.path.exists(fullname)):
                    return HttpResponse(str(files[i]) + "文件已经存在，不能再添加！")
                else:
                    idx = fullname.rfind('\\')
                    if(idx>0):
                        if(os.path.exists(fullname[0:idx])==False):
                            return HttpResponse(str(fullname[0:idx]) + "所在的目录不存在，不能直接添加！")
                        
                if('.' in files[i]):
                    products = ""
                    filename = files[i].split('\\')[-1]
                    
                    for j in range(0, len(links)):
                        if(filename in links[j]):
                            products += links[j].split('\\')[-2] + ","
                    if(len(products)>0 and products[-1]==","):
                        products = products[:len(products)-1]
                            
                    newfiles_dir[files[i]] = products
                else:
                    newfiles_dir[files[i]] = ''
                
        log_Msg("newfiles_dir:" + str(newfiles_dir))
        
        ret = 0
        for file_key in newfiles_dir.keys():
            dir_list = file_key.split('\\')
            file_dir = '\\'.join(dir_list[i] for i in range(0, len(dir_list)-1))
            cc_dir = cc_branch + '\\'+ file_dir
            log_Msg("cc_dir:" + str(cc_dir))
        
            #connect hz_rd_build3 to create new files on CC
            ret |= cc_action(cc_dir, dir_list[-1], newfiles_dir[file_key])
            copyfile()
            log_Msg("ret:" + str(ret))

        if ret == 0:
            form = NewFileForm(data)
            if form.is_valid():
                form.save()
                return HttpResponse("添加文件成功！")
            else:
                return HttpResponse("表单无效，添加文件失败！")
        else:
            errorMsg = ""
            if ret == 1:
                errorMsg = "连接服务器出现问题，添加文件失败！"
            elif ret == 2:
                errorMsg = "ClearCase处理有问题，添加文件失败！"
            elif ret == 3:
                errorMsg = "添加过程中出现问题，添加文件失败！"
            return HttpResponse(errorMsg)
    
    return render_to_response('newfile_add.html', \
                              {'title': u'Create new file on ClearCase', 'form':form, 'submitter':submitter},  \
                              context_instance=template.RequestContext(request))

def query(request):
    form = QueryForm()
    t_err = 0
    t_err1 = 0
    
    if request.POST:
        records = newfile.objects.all()
        data=request.POST.copy()
        
        submitter_name = data['submitter_name'].strip()
        mr_id = data['mr_id'].strip()
        filename = data['filename'].strip()
        vob_branch = data['vob_branch']
        
        submitTime_start = data['submitTime_start'].strip()
        if submitTime_start:
            t_err = error_msg(submitTime_start)
        submitTime_end = data['submitTime_end'].strip()
        if submitTime_end:
            t_err1 = error_msg(submitTime_end)
            
        if t_err or t_err1:#如果遇到异常，设置错误信息
            form.is_valid()
            if t_err:
                form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err
            if t_err1:
                form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err1
        else:
            if len(submitter_name) != 0:
                records = records.filter(submitter = submitter_name)
            if len(mr_id) != 0:
                records = records.filter(mrs = mr_id)
            if len(vob_branch) !=0:
                records = records.filter(vob_branch = vob_branch)
            if len(filename) != 0:
                records = records.filter(Q(new_file_list__contains = filename) | Q(link_file_list__contains = filename))
            if len(submitTime_start) != 0:
                records = records.filter(submit_time__gte = submitTime_start)
            if len(submitTime_end) != 0:    
                records = records.filter(submit_time__lte = submitTime_end)
            
            return render_to_response('query_empty_file_answer.html', \
                    {'title': u'CC新建文件查询结果', 'records': records.order_by('-submit_time')},\
                    context_instance=template.RequestContext(request))
            
    return render_to_response('query_empty_file.html', \
            {'form':form}, \
        context_instance=template.RequestContext(request))

def error_msg(data):
    error = ""#异常信息
    err = False
 
    m = re.match('(\d{4})-(\d{1,2})-(\d{1,2})$', data)
    if m is not None:
        if ((int(m.group(2))<1) or (int(m.group(2))>12) or \
            (int(m.group(3)) <1) or (int(m.group(3))>31)):
            err = True
    else:
        err =True
    
    if err:
        error = u'无效的时间:%s，请输入一个 YYYY-MM-DD 格式的有效日期。' %data
   
    return error