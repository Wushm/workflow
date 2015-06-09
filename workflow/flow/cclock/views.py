# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from workflow.flow.cclock.forms import CCLockFlowForm, RfbMrForm, QueryForm
from workflow.flow.cclock.models import MR, CCLockFlow
from workflow.settings import get_mssql_conn, approvers, CCLOCK_URL, \
        APPROVE_CCLOCK_URL, logging, Rfb_MR_CMD, PERL_SCRIPT_DIR
from workflow.MrReview.models import Review
#from django.core.mail import send_mail
from workflow.send_mail import send_mail
from workflow.vob_config import jobnumber_name
from workflow.portal.get_user_info import get_user_info 



def get_user_cname(username):
    user = User.objects.get(username = username)
    if user.first_name is None:
        return jobnumber_name[username][0] 
    else:
        return user.first_name


def get_user_email(username):
    users = User.objects.filter(username = username)
    if  len(users) == 0:
        return ""
    user_obj = User.objects.get(username = username)
    if len(user_obj.email) == 0:
        user_info  = get_user_info(username)
        if user_info is None:
            from MySQLdb import *    
            sql = "SELECT email FROM `cdb_members` WHERE username = '%s'" % username
            from workflow.settings import get_discuz_conn
            conn = get_discuz_conn()
            cur=conn.cursor()#MySQLdb.cursors.DictCursor
            cur.execute(sql)
            ret=cur.fetchone()
            email = ""
            if ret:
                email = ret[0]
            conn.close()
            return email
        else:
           user_obj.email = user_info['email'] 
           user_obj.first_name = user_info['c_name']
           user_obj.last_name = user_info['e_name']
           user_obj.save()
           return user_obj.email
    else:
        return user_obj.email

#TODO 显示需要审核的记录数
def _can_approve(u, cclock):
    """
    是否有审核权限
    可能是没权限，也可能是已经审核通过
    """
    if cclock.approve_result:
        return False
    def get_v_from_approvers(k):
        if k == 'None':
            return []
        if k:
            return approvers[k]
        return []
    return (u.username in get_v_from_approvers(cclock.vob_branch_1)) or \
            (u.username in get_v_from_approvers(cclock.vob_branch_2)) or \
            (u.username in get_v_from_approvers(cclock.vob_branch_3)) or \
            (u.username in get_v_from_approvers(cclock.vob_branch_4)) or \
            (u.username in get_v_from_approvers(cclock.vob_branch_5)) or \
            (u.username in get_v_from_approvers(cclock.vob_branch_6)) 

@login_required
def my_cclocks(request):
    """
    显示当前用户提交的cclock
    """
    u = request.user
    cclocks = u.my_cclocks.all()
    q_approve_result = request.GET.get('q_approve_result', '')
    if q_approve_result:
        if q_approve_result == 'u':
            cclocks = cclocks.filter(approve_result__isnull=True)
        else:
            cclocks = cclocks.filter(approve_result__exact=q_approve_result)
    return render_to_response('cclock/my_cclocks.html', \
            {'title': u'ClearCase Lock 改动电子流', 'cclocks': cclocks.order_by('-submit_time'),\
            'q_approve_result': request.GET.get('q_approve_result', '')}, \
        context_instance=template.RequestContext(request))


def _format_bugs(bugs):
    def verify_mrid(mrid):
        import re
        embedded_rawstr = r"""^[A-Z_]{2,4}\d{5,12}"""
        match_obj = re.search(embedded_rawstr, mrid)
        if match_obj:
            return True
        return False

    def command_mr(bug):
        command_mrs_id = (u'ONS00042568',u'ONS00042567',u'ONS00042566',u'ONS00042565',u'ONS00042564', \
                     u'ONS00042563',u'ONS00042562',u'ONS00042605',u'ONS00042589')
        i = 0
        command_mr = ''
        for command_mr in command_mrs_id:
            mr = bug[0:11]
            logging.debug("mr:" + mr)
            if bug.find(command_mr) > -1:
                return True
        return False
    """
    格式化MR
    """
    #[u'ONS000000', u'ONS000001']
    error = ""#异常信息
    form_bugs = []#form字段的内容
    if bugs == '':
        error = u'对不起，没有MR不允许提交电子流,请填写至少一个MR,没有相应MR，先新建一个MR'
        return error,form_bugs
    bug_list=bugs.splitlines()#.split("\n")
    bug_list=[e.strip().upper() for e in bug_list if e.strip()]
   
   
    for b in bug_list:
        if not verify_mrid(b):
            #如果MR不存在...
            error = u'无效的MR：%s' % b
            break        
        mr=None
        try:
            mr=MR.objects.get(mr_id=b)
        except:
            pass
        if not mr:
            mr = MR(mr_id=b,mr_headline='',mr_state='none')
            mr.save()
            form_bugs.append(mr.mr_id)
        form_bugs.append(mr.mr_id)
    return error, form_bugs

def _do_upload(files):
    """
    上传文件
    上传文件的描述形式
    服务器文件名|原始文件名
    """
    def encode_filename(fn):
        import urllib
        fn = fn.encode('UTF-8')
        return urllib.quote(fn)
    from workflow.settings import UPLOAD_DIR
    import time
    import os
    #import urllib
    import random
    ret = ""
    for file in files:
        ext = file.name.split('.')[-1]
        filename=str(time.time()).replace('.','_')+str(random.randrange(0,99999,1))+'.'+ext
        ret += encode_filename(file.name) + '|' + filename + '\r\n'#urllib.quote(file.name)
        filename = os.path.join(UPLOAD_DIR, filename)
        f = open(filename, 'wb+')
        for chunk in file.chunks():
            f.write(chunk)
    return ret.strip()

def _get_all_approver_mails(cclock):
    """
    获取所有的审核人
    """
    def get_all_approver_mails(vob_branch):
        emails = {}
        if vob_branch:
           from workflow.VobConfig.views import branch_approvers_email
           return branch_approvers_email(vob_branch)
    emails = get_all_approver_mails(cclock.vob_branch_1)
    emails.update(get_all_approver_mails(cclock.vob_branch_2))
    emails.update(get_all_approver_mails(cclock.vob_branch_3))
    emails.update(get_all_approver_mails(cclock.vob_branch_4))
    emails.update(get_all_approver_mails(cclock.vob_branch_5))
    emails.update(get_all_approver_mails(cclock.vob_branch_6))
    return emails

#added by rsy
def _get_mrreview_list_from_workflow(cclock):
    total_list = []
    cclock = cclock.order_by('-submit_time')
    review_records = Review.objects.all()
    
    for cclock_record in cclock:
        found = False
        row = []
        review_row = {}
        
        for review_record in review_records:
            if(cclock_record.id == review_record.workflow_id):
                review_row['op'] = "view"
                review_row['text'] = "Query"
                found = True
                break
        
        if(found == False):
            review_row['op'] = "add"
            review_row['text'] = "Add"
            
        row.append(cclock_record)
        row.append(review_row)
        
        total_list.append(row)
        
    return total_list
            


def get_checkuser_code(username, approve_check_code):
    import md5
    m = md5.new()
    s = username + "just" + approve_check_code
    m.update(s)
    checkuser = m.hexdigest()
    return checkuser

# 设置URL
def gen_approve_url(username, approve_check_code, cclock_id, action):
    """
    生成审核的url
    """
    checkuser = get_checkuser_code(username, approve_check_code)
    url_params = "?cclock_id=%s&approve_check_code=%s&username=%s&checkuser=%s" % \
            (cclock_id, approve_check_code, username, checkuser)
    from workflow.settings import DO_APPROVE_CCLOCK_URL
    base_url = DO_APPROVE_CCLOCK_URL % (cclock_id)
    if 'reject' == action:
        url_params += '&action=%s' % 'x'
    else:
        url_params += '&action=%s' % 'o'
    return base_url + url_params

def _send_new_apply_notice_mail(cclock):
    """
    发送邮件通知审核人和自己
    """
    
    username = cclock.submitter.username
    CN_Name = get_user_cname(username)
    emails = _get_all_approver_mails(cclock)
    subject = u'请您审核 [%s] ClearCase改动请求 %s' % (CN_Name,cclock.title)
    message = u"""请您审核 ClearCase改动请求 “{{cclock.title}}”
{% load cclock_filters %}
{% load cclock_tags %}    
通过审核：{{pass_url}}
驳回：{{reject_url}}
查看具体请求信息：{{cclock_url}}
===================详细信息===================
申请人：{{cclock.submitter.username}}
Vob branch 1：{{cclock.vob_branch_1}}
Vob branch 2：{{cclock.vob_branch_2}}
Vob branch 3：{{cclock.vob_branch_3}}
Vob branch 4：{{cclock.vob_branch_4}}
Vob branch 5：{{cclock.vob_branch_5}}
Vob branch 6：{{cclock.vob_branch_6}}
MR列表：{{cclock.bugs.all|str_bugs}}
附件：{{cclock.attachments|attachments|safe}}
描述：{{cclock.descn}}"""
    t = template.Template(message)
    from workflow.settings import SERVER_EMAIL
    for username, email in emails.items():
        context = template.Context(\
                {'cclock': cclock, \
                'cclock_url': APPROVE_CCLOCK_URL % str(cclock.id),\
                'pass_url': gen_approve_url(username, cclock.approve_check_code, cclock.id, action='ok'),\
                'reject_url': gen_approve_url(username, cclock.approve_check_code, cclock.id, action='reject')})
        context.autoescape = False
        message = t.render(context)
        try:
            #send_mail(subject, message, SERVER_EMAIL, [email], fail_silently=False)
            send_mail(subject,message,email)
            logging.debug("[send mail succes, username, email]" + username + ' | ' + email)
        except:
            logging.debug("[send mail fail, username, email]" + username + ' | ' + email)


def update_cclock_vob_config(cclock):
    from workflow.VobConfig.views import update_vob_config
    update_vob_config(cclock.vob_branch_1)
    update_vob_config(cclock.vob_branch_2)
    update_vob_config(cclock.vob_branch_3)
    update_vob_config(cclock.vob_branch_4)
    update_vob_config(cclock.vob_branch_5)
    update_vob_config(cclock.vob_branch_6)

@login_required
def add(request):
    """
    提交新请求
    """
    form = CCLockFlowForm()
    bugs=""
    title = ""
    if request.POST:
        data=request.POST.copy()
        bugs=data['bugs']
        t_err, form_bugs = _format_bugs(data['bugs'])
        data.setlist('bugs', form_bugs)
        from workflow.flow.cclock.helper import get_mr_infos
        if form_bugs != []:
           mr_info = get_mr_infos(form_bugs[0]) 
           title =form_bugs[0] + '  ' + mr_info.headline.decode("GBK")
           data['title'] = title[0:99]
        else:
           data['title'] = u'No MR number'
        data['submitter']=str(request.user.id)
        import random
        random.seed()
        data['approve_check_code'] = str(random.randint(0,999999999))
        #FIXME 即使是在表单提交失败的情况下，文件依旧不会被删除。
        #FIXME 不过考虑到上传的文件不会很多，这里不做太多的考虑
        #上传附件
        attachments_descn = _do_upload(request.FILES.getlist('attachment'))
        data['attachments']=attachments_descn
        form = CCLockFlowForm(data)
        if t_err:#如果遇到异常，设置错误信息
            form.is_valid()
            form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err
        elif form.is_valid():
            cclock = form.save()
            update_cclock_vob_config(cclock)
            _send_new_apply_notice_mail(cclock)
            return HttpResponseRedirect('../?q_approve_result=u')
    return render_to_response('cclock/cclocks_edit.html', \
            {'title': u'ClearCase Lock 改动电子流', 'form':form, 'bugs':bugs}, \
        context_instance=template.RequestContext(request))

@login_required
def view(request, id):
    """
    查看
    """
    #added by rsy
    reviewinfo = Review.objects.filter(workflow_id=id)
    if not reviewinfo:
        mr_review_add = True
    else:
        mr_review_add = False
    
    cclock=CCLockFlow.objects.get(id=id)
    submitter_email = get_user_email(cclock.submitter.username)
    CN_Name = get_user_cname(cclock.submitter.username)
    #CN_Name = unicode(jobnumber_name[cclock.submitter.username][0],'utf-8')
    return render_to_response('cclock/cclocks_view.html', \
            {'title': u'ClearCase Lock 改动电子流', 'original': cclock,\
            'submitter_email':submitter_email,\
            'CN_Name':CN_Name,\
            'mr_review_add':mr_review_add, \
            'can_approve': _can_approve(request.user, cclock)}, \
        context_instance=template.RequestContext(request))

def query(request):
    form = QueryForm(initial={'vob_branch':'test'})
    cclocks = CCLockFlow.objects.all()
    if request.POST:
        data=request.POST.copy()
        submitter_name = data['submitter_name'].strip()
        approver_name = data['approver_name'].strip()
        mr_id = data['mr_id'].strip()
        vob_branch = data['vob_branch']
        if len(submitter_name) != 0:
            cclocks = cclocks.filter(submitter__username = submitter_name) 
        if len(approver_name) != 0:
            cclocks = cclocks.filter(who_approver__username = approver_name) 
        if len(mr_id) != 0:
            cclocks = cclocks.filter(bugs__mr_id = mr_id)
        if vob_branch != 'test':
            q_branchs = ",".join(["'"+vob_branch.replace('\\', '\\\\')+"'"]) 
            cclocks = cclocks.extra(\
                    where=[" (vob_branch_1 in (%s) or vob_branch_2 in (%s) or vob_branch_3 in (%s) or vob_branch_4 in (%s) or vob_branch_5 in (%s) or vob_branch_6 in (%s)) " \
                    % (q_branchs, q_branchs, q_branchs, q_branchs, q_branchs, q_branchs)])
            
        #added by rsy
        total_list = _get_mrreview_list_from_workflow(cclocks)
        
        return render_to_response('cclock/todo_cclocks.html', \
                #{'title': u'ClearCase Lock 改动电子流', 'cclocks': cclocks.order_by('-submit_time'), \
                {'title': u'ClearCase Lock 改动电子流', 'cclocks': total_list, \
                'q_approve_result': request.GET.get('q_approve_result', '')}, \
            context_instance=template.RequestContext(request))
    return render_to_response('cclock/cclocks_query.html', \
            {'form':form}, \
        context_instance=template.RequestContext(request))

def _username2vob_branchs(username):
    """
    获取用户可以审核的branchs
    """
    ret=[]
    for k, v in approvers.items():
        if username in v:
            ret.append(k)
    return ret

@login_required
def todo_cclocks(request):
    """
    显示等待当前用户审核的cclock
    """
    #user->vob_branch
    #查看当前用户可以审核的branch
    #branch1/2/3=branch的mr
    u = request.user
    username = u.username
    branchs = _username2vob_branchs(u.username)
    q_branchs = ",".join(["'"+e.replace('\\', '\\\\')+"'" for e in branchs])    
    if not q_branchs:
        q_branchs = "'=just='"#如果为空，必须填一个随意的值，不然会出错。
    cclocks = CCLockFlow.objects.all()
    # 如果是超级管理员，显示所有
    if True:#not u.is_superuser
        cclocks = cclocks.extra(\
                where=[" (vob_branch_1 in (%s) or vob_branch_2 in (%s) or vob_branch_3 in (%s) or vob_branch_4 in (%s) or vob_branch_5 in (%s) or vob_branch_6 in (%s)) " \
                % (q_branchs, q_branchs, q_branchs, q_branchs, q_branchs, q_branchs)])
    q_approve_result = request.GET.get('q_approve_result', '')
    if q_approve_result:
        if q_approve_result == 'u':
            cclocks = cclocks.filter(approve_result__isnull=True)
        else:
            cclocks = cclocks.filter(approve_result__exact=q_approve_result)
            
    #added by rsy
    total_list = _get_mrreview_list_from_workflow(cclocks)
        
    return render_to_response('cclock/todo_cclocks.html', \
            #{'title': u'ClearCase Lock 改动电子流', 'cclocks': cclocks.order_by('-submit_time'), \
            {'title': u'ClearCase Lock 改动电子流', 'cclocks': total_list, \
            'q_approve_result': request.GET.get('q_approve_result', '')}, \
        context_instance=template.RequestContext(request))

def view_all_approved_result(request):
    """
    显示等待当前用户审核的cclock
    """
    #user->vob_branch
    #查看当前用户可以审核的branch
    #branch1/2/3=branch的mr
    branchs = _username2vob_branchs('admin')
    q_branchs = ",".join(["'"+e.replace('\\', '\\\\')+"'" for e in branchs])    
    if not q_branchs:
        q_branchs = "'=just='"#如果为空，必须填一个随意的值，不然会出错。
    cclocks = CCLockFlow.objects.all()
    # 如果是超级管理员，显示所有
    if True:#not u.is_superuser
        cclocks = cclocks.extra(\
                where=[" (vob_branch_1 in (%s) or vob_branch_2 in (%s) or vob_branch_3 in (%s) or vob_branch_4 in (%s) or vob_branch_5 in (%s) or vob_branch_6 in (%s)) " \
                % (q_branchs, q_branchs, q_branchs, q_branchs, q_branchs, q_branchs)])
        
    #added by rsy
    total_list = _get_mrreview_list_from_workflow(cclocks)
        
    return render_to_response('cclock/todo_cclocks.html', \
            #{'title': u'ClearCase Lock 改动电子流', 'cclocks': cclocks.order_by('-submit_time'), \
            {'title': u'ClearCase Lock 改动电子流', 'cclocks': total_list, \
             'q_approve_result': 'o'}, \
        context_instance=template.RequestContext(request))

def _send_approve_mail(cclock, action):
    """
    发送审核邮件通知
    """
    #from django.core.mail import send_mail
    action_descn = u"驳回"
    if 'o' == action:
        action_descn = u"通过"
    subject = u'您提交的 ClearCase改动请求 “%s” 已 %s' % (cclock.title, action_descn)
    message = u"""您提交的 ClearCase改动请求 “%s” 已 %s
    审核备注信息：%s
%s""" % (cclock.title, action_descn, CCLOCK_URL % str(cclock.id), cclock.approve_note)
    from workflow.settings import SERVER_EMAIL
    username = cclock.submitter.username
    email = get_user_email(cclock.submitter.username)
    try:
        #send_mail(subject, message, SERVER_EMAIL,
        #    [email], fail_silently=False)
        send_mail(subject,message,email)
    except:
        logging.debug("[send mail fail, username, email]" + username + ' | ' + email)


def _auto_login(request, username):
    """
    根据用户名自动登陆
    """
    u = User.objects.get(username=username)
    bak_password = u.password
    try:
        tmp_pswd='123456'
        u.set_password(tmp_pswd)
        u.save()
        from django.contrib import auth
        u = auth.authenticate(username=username,\
            password=tmp_pswd)
        auth.login(request, u)
    except:
        pass
    u.password=bak_password
    u.save()#还原密码
    return True

#@login_required
def approve(request, id, action=''):
    """
    审核
    """
    cclock=CCLockFlow.objects.get(id=id)
    action = request.GET.get('action', 'u')
    approve_note = request.GET.get('approve_note', 'u')
    if not request.user.is_authenticated():
        approve_check_code=request.GET.get('approve_check_code', '')
        username = request.GET.get('username', '')
        checkuser = request.GET.get('checkuser', '')
        test_checkuser = get_checkuser_code(username, approve_check_code)
        if (approve_check_code==cclock.approve_check_code) and (test_checkuser == checkuser):
            _auto_login(request, username) #自动登陆
    if "o" == action:
        action_descn = u"通过审核"
    if "x" == action:
        action_descn = u"驳回"
    if "u" == action:
        message = u'更新工作流“%s”' % cclock.title
        return HttpResponseRedirect('../cclock_update')
    if cclock.approve_result:            
        return HttpResponse("该请求已完成审核，无需要再次审核")
    if not _can_approve(request.user, cclock):#如果没有审核权限
        return HttpResponse("您没有审核权限")
    
    #需要判断审批通过时是否填写MR review信息 rsy
    if "o" == action:
        reviewinfo = Review.objects.filter(workflow_id=id)
        if not reviewinfo:
            return HttpResponse("您必须填写MR review信息")
    
    message = ""
    if request.POST or action:
        data = request.POST.copy()
        if not action:
            action = data['action']
        if 'o' == action:
            cclock.approve_result = action
            message = u'工作流“%s”审核通过' % cclock.title
            #request.user.message_set.create(message=u'工作流“%s”审核通过' % cclock.title)
        if 'x' == action:
            cclock.approve_result = action
            message = u'驳回工作流“%s”' % cclock.title
            #request.user.message_set.create(message=u'驳回工作流“%s”' % cclock.title)
        cclock.approve_note = approve_note
        from datetime import datetime
        cclock.approve_time = datetime.now()#审批时间
        cclock.who_approver = request.user
        #发送邮件
        from workflow.flow.cclock.lock.views import exec_assign
        
        ret_code = '-5' # initial to nozero, means failed.
        ret_str = "unkonw-reason"
	if cclock.who_approver.username != 'admin' and cclock.who_approver.username == cclock.submitter.username:
	    ret_str = "approve falile,you can't approve to limit for yourself"
	    ret_code = '-3'
        elif 'o' == action: 
	    if cclock.vob_branch_1:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_1)#开通权限
            if cclock.vob_branch_2:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_2)#开通权限
            if cclock.vob_branch_3:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_3)#开通权限
            if cclock.vob_branch_4:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_4)#开通权限
            if cclock.vob_branch_5:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_5)#开通权限
            if cclock.vob_branch_6:
                ret_code, ret_str = exec_assign(cclock.submitter.username, cclock.vob_branch_6)#开通权限
        elif 'x' == action:
            ret_code = '0'
        elif 'u' == action:
            ret_code = '-1'
            return HttpResponseRedirect('../cclock_update')
        # 根据返回值判断是否开通成功
        if ret_code == '0': 
            _send_approve_mail(cclock, action)
            cclock.save()
        else:
            from django.utils.safestring import mark_safe
            message = mark_safe(u'处理失败：<br/>%s' % ret_str)
            request.user.message_set.create(message=message)
            return HttpResponseRedirect('../../?q_approve_result=u')
    if message:
        request.user.message_set.create(message=message)
    return HttpResponseRedirect('../../?q_approve_result=u')
    """return render_to_response('cclock/check.html', \
            {'title': u'ClearCase Lock 改动电子流', 'original': cclock, \
            'action': action, 'action_descn': action_descn}, \
        context_instance=template.RequestContext(request))"""

descn = u"""MR:ONS00000
Modifiers:admin
Problem caused:中文
bbb
ccc
Resolution:AAA
BBB
CCC

MR:ONS111111
Modifiers:admin1
Problem caused:aaa1
bbb1
ccc1
Resolution:AAA1
BBB1
CCC1
"""

@login_required
def rfb_mr(request, id):
    from helper import parse_cc_descn, mr_infos2csv
    form = RfbMrForm(initial={'introduction_phase':'S/W Implementation', 
        'impacted_unit':'Source Code'})
    cclock=CCLockFlow.objects.get(id=id)
    help_mr_infos, mr_infos = parse_cc_descn(cclock.descn)
    #help_mr_infos = parse_cc_descn(descn)
    help_mr_infos_json = simplejson.dumps(help_mr_infos, ensure_ascii = False)
    mr_infos_json = simplejson.dumps(mr_infos, ensure_ascii = False)
    email = get_user_email(cclock.submitter.username)
    user_name = email[0:email.find('@')]
    user_name = user_name.replace(".","_")
    if request.POST:
        data=request.POST.copy()
        form = RfbMrForm(data)
        if form.is_valid():
            succ = False
            #将info导出为CSV
            from datetime import datetime
            fn = 'c:/%s.csv' % datetime.now().microsecond
            mr_infos2csv(fn, form.cleaned_data)
            import subprocess
            cmd = Rfb_MR_CMD % (request.POST['cq_username'], \
                    request.POST['cq_password'], 'ONS', fn)
            p=subprocess.Popen(cmd, cwd=PERL_SCRIPT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            rets = p.communicate()
            ret = rets[0].strip() + rets[1].strip()
            ret = ret.strip()
            if "== create session fail ==" == ret:
                #return HttpResponse("用户名或密码不正确，无法连接Clear Quest");
                request.user.message_set.create(message=u"用户名或密码不正确，无法连接Clear Quest")
            elif "== OK ==" == ret:
                succ = True
                request.user.message_set.create(message=u"更新成功")
            else:
                request.user.message_set.create(message= u"未知错误:" + ret)
            #------------------
            if succ:
                return HttpResponseRedirect('../../?q_approve_result=o')
    return render_to_response('cclock/rfb_mr.html', \
            {'title': cclock.title, 'form':form,
                'help_mr_infos_json': help_mr_infos_json,
                'help_mr_infos': help_mr_infos,
                'mr_infos_json': mr_infos_json,
                'mr_infos': mr_infos,
                'user_name':user_name,
                'End':''}, \
        context_instance=template.RequestContext(request))


def parse_bugs(cclock_bugs):
    """
    MR列表输出需要对cclock的bugs进行格式化
    """
    t_bugs = ''
    lines = cclock_bugs.split(",")
    for line in lines:
        if line == lines[0]:
            t_bugs += line
        else:
            t_bugs += '\r\n' + line
    return t_busg
    
def update(request, id):
    """
    更新
    """
    form = CCLockFlowForm()
    cclock = CCLockFlow.objects.get(id=id)
    request_username = str(request.user.username)
    #bugs = ''
    #bugs = parse_bugs(cclock.bugs.value_to_string(MR))
    if request.POST:
        #return HttpResponseRedirect('../?q_approve_result=u')
        data=request.POST.copy()
        bugs=data['bugs']
        t_err, form_bugs = _format_bugs(data['bugs'])
        data.setlist('bugs', form_bugs)
        files = request.FILES.getlist('attachment')
        #增加的附件会覆盖原有的附件
        if len(files) != 0:
            attachments_descn = _do_upload(request.FILES.getlist('attachment'))
            cclock.attachments = attachments_descn
        old_cclock = cclock
        cclock.descn = data['descn']
        cclock.vob_branch_1 = data['vob_branch_1']
        cclock.vob_branch_2 = data['vob_branch_2']
        cclock.vob_branch_3 = data['vob_branch_3']
        cclock.vob_branch_4 = data['vob_branch_4']
        cclock.vob_branch_5 = data['vob_branch_5']
        cclock.vob_branch_6 = data['vob_branch_6']
        if data['bugs'] != []:
            cclock.title = data['title']
            cclock.bugs.add(data['bugs'])  
        cclock.save()
        submitter_username = cclock.submitter.username
        if t_err:#如果遇到异常，设置错误信息
            form.is_valid()
            form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err
        else:
            if (submitter_username == request_username):
                print "***************send mail*********"
                _send_new_apply_notice_mail(cclock)
            return HttpResponseRedirect('../?q_approve_result=u') 
    return render_to_response('cclock/cclocks_update.html', \
        {'title': u'ClearCase Lock 改动电子流', 
             'form': form,
             'cclock': cclock }, \
        context_instance=template.RequestContext(request))

MR_INFO = {'mr_id':'','title':'','descn':''}
def newFlow2newMR(request):
    mr_id = MR_INFO['mr_id']
    mr_descn = MR_INFO['descn']
    mr_title = MR_INFO['title']
    form = CCLockFlowForm()
    mr_infos = simplejson.dumps(MR_INFO, ensure_ascii = False)
    bugs=""
    if request.POST:
        data=request.POST.copy()
        bugs=data['bugs']
        t_err, form_bugs = _format_bugs(data['bugs'])
        data.setlist('bugs', form_bugs)
        from workflow.flow.cclock.helper import get_mr_infos
        if form_bugs != []:
           mr_info = get_mr_infos(form_bugs[0]) 
           title =form_bugs[0] + '  ' + mr_info.headline.decode("GBK")
           data['title'] = title[0:99]
        else:
           data['title'] = u'No MR number'
        data['submitter']=str(request.user.id)
        import random
        random.seed()
        data['approve_check_code'] = str(random.randint(0,999999999))
        #FIXME 即使是在表单提交失败的情况下，文件依旧不会被删除。
        #FIXME 不过考虑到上传的文件不会很多，这里不做太多的考虑
        #上传附件
        attachments_descn = _do_upload(request.FILES.getlist('attachment'))
        data['attachments']=attachments_descn
        form = CCLockFlowForm(data)
        if t_err:#如果遇到异常，设置错误信息
            form.is_valid()
            form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err
        elif form.is_valid():
            cclock = form.save()
            _send_new_apply_notice_mail(cclock)
            MR_INFO['mr_id'] = ''
            MR_INFO['title'] = ''
            MR_INFO['descn'] = ''
            return HttpResponseRedirect('../?q_approve_result=u')
    return render_to_response('cclock/cclocks_newFlow2newMR.html', \
            {'title': u'ClearCase Lock 改动电子流','form':form, 'bugs':bugs,\
            'mr_infos':mr_infos}, \
        context_instance=template.RequestContext(request))
