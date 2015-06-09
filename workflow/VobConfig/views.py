# Create your views here.
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from workflow.VobConfig.form import *
from workflow.VobConfig.models import CVobConfig

def get_branch_choices():
    branch_choices = (('','---------'),)
    all_branch_configs = CVobConfig.objects.all()
    for branch in all_branch_configs:
        if branch.devStatus == 'close':
            continue
        name = branch.branch
        choice = branch.choices
        branch_choices = branch_choices + ((name,choice),)
    return branch_choices

def get_all_branch_status():
    branch_status = {}
    all_branch_configs = CVobConfig.objects.all()
    for branch in all_branch_configs:
        name = branch.branch
        stat = branch.devStatus
        if stat == r'dev':
            branch_status[name] = 1
        elif stat == r'maintai=':
            branch_status[name] = 2
        elif stat == r'close':
            branch_status[name] = 3
        else:
            branch_status[name] = 0
    return branch_status
    
def get_all_branch_release_number():
    release_number = {}
    all_branch_configs = CVobConfig.objects.all()
    for branch in all_branch_configs:
        name = branch.branch
        release_number[name] = branch.release_number
    return release_number

def approvers(vob_branch):
    approvers=()
    vob_config = CVobConfig.objects.filter(branch = vob_branch)
    for branch in vob_config:
        users = branch.approvers.values()
        for user in users:
            approvers = approvers + user['username']
    return approvers

def approvsers_name(vob_branch):
    approvers=()
    vob_config = CVobConfig.objects.filter(branch = vob_branch)
    for branch in vob_config:
        users = branch.approvers.values()
        for user in users:
            approvers = approvers + user['firstname']
    return approvers


def update_all_vob_config():
    from workflow.settings import approvers,vob_masters,approve_servers,vob_branch_status,vob_branch_release_number
    vob_configs = CVobConfig.objects.all()
    for config in vob_configs:
        #step1: 设置approvers
        users = config.approvers.values()
        approvers[config.branch] = ()
        for user in users:
            approvers[config.branch] = approvers[config.branch] + (user['username'],)
        #step2: 设置vob_masters
        users = config.masters.values()
        vob_masters[config.branch] = ()
        for user in users:
            vob_masters[config.branch] = vob_masters[config.branch] + (user['username'],)
        #step3:设置服务器
        approve_servers[config.branch] = ''   
        approve_servers[config.branch] = config.servers
        vob_branch_status[config.branch] = config.devStatus
        vob_branch_release_number[config.branch] = config.release_number

def update_vob_config(vob_branch):
    from workflow.settings import approvers,vob_masters,approve_servers
    vob_configs = CVobConfig.objects.filter(branch = vob_branch)
    if vob_branch:
        for config in vob_configs:
            approvers[config.branch] = ()
            users = config.approvers.values()
            for user in users:
                approvers[config.branch] = approvers[config.branch] + (user['username'],)
            users = config.masters.values()
            vob_masters[config.branch] = ()
            for user in users:
                vob_masters[config.branch] = vob_masters[config.branch] + (user['username'],)
            approve_servers[config.branch] = ''   
            approve_servers[config.branch] = config.servers   
        
def branch_approvers_email(vob_branch):
    emails = {}
    vob_config = CVobConfig.objects.filter(branch = vob_branch)
    for branch in vob_config:
        users = branch.approvers.values()
        for user in users:
            if user['email']:
                emails[user['last_name']] = user['email']
    return emails
                
    
def server(vob_branch):
    vob_config = CVobConfig.objects.filter(branch = vob_branch)
    return vob_config.server

def master(vob_branch):
    masters = ()
    vob_config = CVobConfig.objects.filter(branch = vob_branch)
    for branch in vob_config:
        users = branch.master.values()
        for user in users:
            masters = masters + user['username']
    return masters

def view(request, id):
    #vob_config = CVobConfig.objects.get('1')
    approvers('test')
    return render_to_response("view.html",\
                              {'title':'分支信息管理',\
                              },\
    context_instance=template.RequestContext(request))
    
def all(request):
    vob_config = CVobConfig.objects.all()
    return render_to_response("view_all.html",\
                              {'title':'分支信息管理',\
                               'vob_config':vob_config},\
    context_instance=template.RequestContext(request))
        
def check_vob(vob_branch):
    vob_branch = CVobConfig.objects.filter(branch = vob_branch)
    if vob_branch:
        return True
    return False
    
    
    
def update_vob_config_data(vob_config,data):
    vob_config.title = data['title']
    vob_config.branch = data['branch']
    vob_config.servers = data['servers']
    vob_config.choices = data['choices']
    vob_config.isLock = data['isLock']
    
def get_all_user(userid_list):
    user_list = []
    for i in range(len(userid_list)):
        print(userid_list[i])
        user = User.objects.get(id = userid_list[i])
        user_list.append(user.id)
    return user_list
    
def update(request,id):
    error_message = ""
    vob_config = CVobConfig.objects.get(id = id)
    form = CVobConfigForm(instance=vob_config)
    form.fields['approvers'].widget.attrs = {'size':25}
    form.fields['masters'].widget.attrs = {'size':25}
    if request.POST:
        data=request.POST.copy()
        #更新title
        vob_config.title = data['title']
        #分支名称不允许改动
        #vob_config.branch = data['branch']
        vob_config.choices = data['choices']
        vob_config.servers = data['servers']
        vob_config.devStatus = data['devStatus']
        vob_config.release_number = data['release_number']
        
        #添加审核人
        user_list = get_all_user(request.POST.getlist("approvers"))

        for user in user_list:
            vob_config.approvers.add(user)
            
        #添加分支权限拥有人    
        user_list = get_all_user(request.POST.getlist("approvers"))
        for user in user_list:
            vob_config.masters.add(user)
            
        #修改分支管理员
        user = User.objects.get(id = data['superAdmin'])
        vob_config.superAdmin = user
        vob_config.save()
        #最后更新vob_config全局变量
        update_vob_config(data['branch'])
        request.user.message_set.create(message=u"更新成功")
        return HttpResponseRedirect("../../all/")
    return render_to_response("update.html",\
                              {'error_message':error_message,\
                                'title':'更新分支信息',\
                               'form':form,\
                               'vob_config':vob_config},\
    context_instance=template.RequestContext(request))
    
    
def add(request):
    error_message = ""
    form = CVobConfigForm()
    form.fields['approvers'].widget.attrs = {'size':25}
    form.fields['masters'].widget.attrs = {'size':25}
    if request.POST:
        data=request.POST.copy()
        form = CVobConfigForm(data)
        print(form.instance.id)
        if check_vob(data['branch']):
            error_message=u'您输入的branch名称已经存在，请重新输入'
        else:
            if form.is_valid():
                vov_config = form.save()
                update_vob_config(data['branch'])
                return HttpResponseRedirect("../all/")
    return render_to_response("add.html",\
                              {'error_message': error_message,\
                                'title':'分支信息管理',\
                               'form':form},\
    context_instance=template.RequestContext(request))

def refresh(request):
    update_all_vob_config()
    return HttpResponseRedirect("../all/")


def get_branch_release_number(vob_branch):
    vob_config = CVobConfig.objects.get(branch = vob_branch)
    return vob_config.release_number
    
  
update_all_vob_config()

    
        