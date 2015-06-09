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
from workflow.NewFile.models import NewFile
from workflow.NewFile.forms import NewFileForm
#TODO ??????????





def _format_file(mr_branch_infos, files):
    """
    格式化需要新添的文件
    """
    bran
    error = "a"#异常信息
    form_files = []#form字段的内容
    file_lists = ""
    directory = ""
    filename = ""
    if file == '':
        error = u'对不起，没有文件路径无法添加空文件，请输入需要新添的文件名及其目录'
        return error,form_files
    file_list=files.splitlines()
    i = 1
    while (i <= 6):
        if 
    for b in file_list:
        print b
        pos = b.rfind('\\')
        print pos
        directory = b[:pos]
        filename = b[pos+1:]
        cmd = "cleartool ls " + directory
        print cmd
        import subprocess
        p=subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.wait()
        rets = p.communicate()
        print rets
        print directory + ", " + filename
        file_lists = file_lists + b + "\n"
    #file_list=[e.strip().upper() for e in file_list if e.strip()]
    return error,file_lists


def get_key_word_blank(s):
    if s.find(':') == -1:
        return '', s
    pos = s.find(':')
    return s[:pos], s[pos+1:]

def parse_blank_descn(descn):
    s=''
    key_words = ['MR', 'vob_branch_1', 'vob_branch_2', 'vob_branch_3', 'vob_branch_4', 'vob_branch_5', 'vob_branch_6']
    mr_branch_infos = {'vob_branch_1':'', 'vob_branch_2':'', 'vob_branch_3':'', 'vob_branch_4':'', 'vob_branch_5':'', 'vob_branch_6':''}
    mr_ids = ""
    mr_infos = ""
    lines = descn.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        key_word, content = get_key_word_blank(line)
        if key_word in key_words:
            if line.startswith('MR:'):
                content = content.strip()
                print content
                mr_ids = mr_ids + content + "\n"
                print mr_ids
            else:
                content = content.strip()
                print content
                mr_branch_infos[key_word] = content
            
    #TODO get mr infos
    mr_branch = ""
    i = 1
    while (i <= 6):
        print mr_branch_infos[key_words[i]]
        if mr_branch_infos[key_words[i]]:
            mr_branch = mr_branch + mr_branch_infos[key_words[i]] + "\n"
        i = i + 1
    return mr_ids, mr_branch, mr_branch_infos

def Copy2Sql(mr_ids, cclock):
    p1 = NewFile()
    p1.id = cclock.id
    p1.mrs = mr_ids
    p1.vob_branch_1 = cclock.vob_branch_1
    p1.vob_branch_2 = cclock.vob_branch_2
    p1.vob_branch_3 = cclock.vob_branch_3
    p1.vob_branch_4 = cclock.vob_branch_4
    p1.vob_branch_5 = cclock.vob_branch_5
    p1.vob_branch_6 = cclock.vob_branch_6
    p1.submitter = cclock.submitter
    p1.approver = cclock.who_approver
    p1.submit_time = cclock.submit_time
    p1.save()


def GetData(blank, cclock):
    data = {}
    blank.vob_branch_1 = data['vob_branch_1'] = cclock.vob_branch_1
    blank.vob_branch_2 = data['vob_branch_2'] = cclock.vob_branch_2
    blank.vob_branch_3 = data['vob_branch_3'] = cclock.vob_branch_3
    blank.vob_branch_4 = data['vob_branch_4'] = cclock.vob_branch_4
    blank.vob_branch_5 = data['vob_branch_5'] = cclock.vob_branch_5
    blank.vob_branch_6 = data['vob_branch_6'] = cclock.vob_branch_6
    blank.submitter = data['submitter'] = cclock.submitter
    blank.approver = data['approver'] = cclock.who_approver
    blank.approve_result = data['approve_result'] = cclock.approve_result
    blank.submit_time = data['submit_time'] = cclock.submit_time
    blank.approve_time = data['approve_time'] = cclock.approve_time
    blank.approve_note = data['approve_note'] = cclock.approve_note
    #blank.descn = data['descn'] = cclock.descn
    return blank, data

@login_required
def add_new(request, id):
    """
    ?????
    """
    cclock=CCLockFlow.objects.get(id=id)
    mr_ids, mr_branch_info = parse_blank_descn(cclock.descn)
    form = NewFileForm()
    bugs=""
    title = ""
    form_files = ""
    if request.POST:
        newfile = NewFile.objects.get(id=id)
        data=request.POST.copy()
        bugs = "hello world"
       
        t_err, form_files = _format_file(newfile, data['file_full_name'])
        t_err = ""
        ##newfile.file_full_name = form_files
        ##newfile.save()
        #data['submitter']=str(request.user.id)
        
        form = NewFileForm(data)
        if t_err:#?????????????
            form.is_valid()
            form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % bugs
        elif form.is_valid():
            cclock = form.save()
            #_send_new_apply_notice_mail(cclock)
            #return HttpResponseRedirect('../?q_approve_result=u')
    else:
        blank=NewFile.objects.get(mrs='ONS00050276')
        #blank.mrs = data['mrs'] = mr_ids
        blank, data=GetData(blank, cclock)
        Copy2Sql(mr_ids, cclock)
        print blank.approve_time, blank.submitter, blank.approve_note, blank.submit_time, blank.approve_result, blank.approver
        #blank.save()
        form = NewFileForm(data)
    print form_files
    return render_to_response('newfile_add.html', \
            {'title': u'ClearCase Lock 增加空文件', 'form':form, 'bugs':mr_ids, 'branch':mr_branch_info, 'filelist':form_files}, \
        context_instance=template.RequestContext(request))