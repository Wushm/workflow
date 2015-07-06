# -*- coding: UTF-8 -*-
from django.contrib.auth import SESSION_KEY, REDIRECT_FIELD_NAME
from django.shortcuts import render_to_response
from django import template
from django.template.context import RequestContext
from django.views.generic.list_detail import object_list
from workflow.portal.forms import LoginForm
from django.http import HttpResponseRedirect
from workflow.settings import SITE_NAME
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from get_user_info import get_user_info

from workflow.VobConfig.views import update_all_vob_config
from workflow.settings import HOST_NAME

@login_required
def index(request):
    update_all_vob_config()
    return render_to_response('index.html', {'title': SITE_NAME}, context_instance=template.RequestContext(request))

def t_list(request):
    from workflow.settings import get_mssql_conn, approvers, CCLOCK_URL, APPROVE_CCLOCK_URL
    from django.http import HttpResponse
    ms_conn=get_mssql_conn()
    ms_cur = ms_conn.cursor()
    query="SELECT id, headline FROM dbo.Dev_Projects_MR_Info where id='%s'" % "ONS00000059"
    ms_cur.execute(query)
    bug=ms_cur.fetchone()
    ms_conn.close()
    #return render_to_response('t_list.html', {'title': SITE_NAME}, context_instance=template.RequestContext(request))
    return HttpResponse(bug[1].decode("GBK"))

def t_edit(request):
    return render_to_response('t_edit.html', {'title': SITE_NAME}, context_instance=template.RequestContext(request))

def _add_user(username, password):
    user_info = None
    user_info = get_user_info(username)
    if user_info is None:
        user_obj = User.objects.create_user(\
            username=username, email='',\
            password=password)
    else:
        user_obj = User.objects.create_user(\
            username=username, email='',\
            password=password)
        user_obj.email = user_info['email']
        user_obj.first_name = user_info['c_name']
        user_obj.last_name = user_info['e_name']
    
    user_obj.is_staff = True
    user_obj.is_superuser = False
    user_obj.save()
    from django.contrib.auth import authenticate
    return authenticate(username=username,\
                        password=password) 

    
def _has_user(username):
    user = None
    try:
        user = User.objects.get(username=username)
    except:
        pass
    return user
    
def  _update_user(username):
    if _has_user(username)  is None:
       return False 
    user_info = None
    user_info = get_user_info(username)
    if user_info is None:
        return True
    else:
        user_obj = User.objects.get(username = username)
        user_obj.email = user_info['email']
        user_obj.first_name = user_info['c_name']
        user_obj.last_name = user_info['e_name']
        return True

#检查和校验用户信息是否存在
def _check_and_update_user_info(username):
    user_obj = _has_user(username)
    #用户不存在
    if user_obj is None:
        return False
    if (len(user_obj.email) == 0):
        user_info = None
        user_info = get_user_info(username)
        user_obj.email = user_info['email']
        user_obj.first_name = user_info['c_name']
        user_obj.last_name = user_info['e_name']
        user_obj.save()
    return True


unicenter_api_path = r'e:/web/xampp/django_project/unicenter'
# 邮件地址由discuz中获取


def login(request):
    # 进行域认证，如果用户不存在创建用户
    error_message=""
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '/')
    form = LoginForm()
    set_email = False
    if request.POST:

        data = request.POST.copy()
        # 做域认证
        username = data['username']
        password = data['password']
        username = username.lower()
        #域用户认证, admin用户除外
        #----------------------------------------------------------------
        if HOST_NAME == 'HZ_RD_WUSHUMING' or HOST_NAME == 'HZ_RD_SERVER':
            import ldap
            if username is not 'admin':
                try:
                    conn = ldap.initialize('ldap://172.18.9.21')
                    conn.simple_bind_s('utscn\\'+username, password)
                    user = _has_user(username)
                    if not user:#如果用户不存在，创建用户
                        user = _add_user(username, password)
                    if user:#更新用户密码，保证使用django内部认证时可以通过
                        user.set_password(password)
                        user.save()
                except:
                    pass    #auth failed
        #校验用户信息是否完整，并自动完善
        if username is not 'admin':
            _check_and_update_user_info(username)
        #-------------------------------------------------------------------
        from django.contrib import auth
        user = auth.authenticate(username=username,\
        password=password)
        if user  is not None:
            auth.login(request, user)
            redirect_to = '/workflow/vob_config/all/'
            return HttpResponseRedirect(redirect_to)
        else:
            error_message=u"您输入的用户名或密码不正确，请使用域账户/密码登陆！"
    return render_to_response('login.html', {'error_message': error_message,
                                             'set_email':set_email,
                                             'title': u'统一认证管理中心'}, context_instance=template.RequestContext(request))
