# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django import template
from workflow.flow.cclock.lock.forms import CCLockForm
from workflow.flow.cclock.lock import clearlock
import approve_log
from workflow.settings import approve_servers, logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def exec_lslock(vobbranch) :
    last_lock = clearlock.ls_lock(vobbranch)
    returnStr = '<strong>Branch & VOB : </strong>' + "<font color='#002BB8'>" + vobbranch + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Remote server : </strong>' + "<font color='#002BB8'>" + approve_servers[vobbranch] + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Lock history : </strong>' + "<font color='#002BB8'>" + last_lock[0] + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Users : </strong>' + "<font color='#002BB8'>" + last_lock[1] + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Return code : </strong>' + "<font color='#002BB8'>" + last_lock[2] + "</font>"
    return returnStr

def exec_assign(eid,vobbranch) :
    logging.debug("[exec_assign | eid, vobbranch]" + eid + ' | ' + vobbranch)
    eid = eid.lower()
    users = ''
    try:
        users = clearlock.getLockExceptUsers(vobbranch)
        if eid.find('hz') != 0 and eid.find('tp') != 0:
            lock_str = 'User id ' + eid +' is invalid'
            ret_code = '1'
        elif (users.find(eid) < 0) :
            users = users + ',' + eid;
            (lock_str,ret_code) = clearlock.replace_lock(vobbranch,users)
        elif (users=='') :
            lock_str = 'Sorry, We Encounter some critical errors!';
            ret_code = '1'
        else :
            lock_str = 'User ' + eid +' already in except list'
            ret_code = '0'#认为是成功的
        if ret_code == '0':#succ
            users = clearlock.getLockExceptUsers(vobbranch)
            if not users.count(eid):
                ret_code = '1'
                lock_str = 'User Limit Apply No Add To Vobbranch'
    except:
        users = 'users' + users + 'xx'
        ret_code = '1'
        lock_str = 'failed, please reference [http://172.18.10.171/rdwiki/images/b/bd/ClearCaseAddLimitProblem.doc]'
    returnStr = '<strong>Branch & VOB : </strong>' + "<font color='#002BB8'>" + vobbranch + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Remote server : </strong>' + "<font color='#002BB8'>" + approve_servers[vobbranch] + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Assign result : </strong>' + "<font color='#002BB8'>" + lock_str + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Current except users : </strong>' + "<font color='#002BB8'>" + users + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Return code : </strong>' + "<font color='#002BB8'>" + ret_code + "</font>" + '<br/>'
    if ret_code=='0' :
        approve_log.logAssign(eid,vobbranch)
    return ret_code, returnStr

def exec_recover(eid,vobbranch) :
    logging.debug("== exec_recover ==")
    eid = eid.lower()
    try:
        users = clearlock.getLockExceptUsers(vobbranch)
        if eid.find('hz') != 0 and eid.find('tp') != 0:
            lock_str = 'User id ' + eid +' is invalid'
            ret_code = '1'
        elif (users.find(eid) > -1) :
            """
            user = ',' + eid
            users = users.replace(user,'')
            """
            logging.debug('[EID, users] #2 ' + eid + ' | ' + users)
            users = users.replace(eid,'')
            users = users.replace(',,', ',')
            users = users.strip(',')
            (lock_str,ret_code) = clearlock.replace_lock(vobbranch,users)
            approve_log.logRecover(eid,vobbranch,False)
            logging.debug('[users, VOBBranch, lock_str, ret_code]' + \
                    users + ' | ' + vobbranch + ' | ' + lock_str + ' | ' + ret_code)
        elif (users=='') :
            lock_str = 'Sorry, We Encounter some critical errors!';
            ret_code = '1'
        else :
            lock_str = 'User ' + eid +' not in except list';
            ret_code = '1'
    except:
        users = ''
        ret_code = '1'
        lock_str = 'failed, unknow error'
    returnStr = '<strong>Branch & VOB : </strong>' + "<font color='#002BB8'>" + vobbranch + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Remote server : </strong>' + "<font color='#002BB8'>" + approve_servers[vobbranch] + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Recover result : </strong>' + "<font color='#002BB8'>" + lock_str + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Current except users : </strong>' + "<font color='#002BB8'>" + users + "</font>" + '<br/>'
    returnStr = returnStr + '<strong>Return code : </strong>' + "<font color='#002BB8'>" + ret_code + "</font>" + '<br/>'
    return ret_code, returnStr

@login_required
def index(request):
    from workflow.settings import admin_user
    if request.user.username not in admin_user:
        return HttpResponse("您没有该权限")
    form = CCLockForm()
    ret = ""
    if request.POST:
        data = request.POST.copy()
        form = CCLockForm(data)
        vobbranch = data['branch']
        eid = data['username']
        action = data['action']
        if 'q' == action:
            ret = exec_lslock(vobbranch)
        if 'assign' == action:
            ret_code, ret = exec_assign(eid,vobbranch)
        if 'recover' == action:
            ret_code, ret = exec_recover(eid,vobbranch)
    return render_to_response('cclock/lock/index.html', \
            {'title': u'ClearCase Lock 改动电子流', 'form': form, 'ret': ret}, \
        context_instance=template.RequestContext(request))
