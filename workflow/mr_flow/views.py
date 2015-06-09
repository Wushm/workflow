# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from workflow.mr_flow.form import CQNewMRForm
from workflow.settings  import New_MR_CMD,PERL_SCRIPT_DIR


def index(request):
    return render_to_response('mr_flow\mr_manage.html', \
            {'title':u'ClearQuest MR电子流管理'}, \
            context_instance=template.RequestContext(request))


def new_mr_info2csv(fn,data):
    import csv
    writer = csv.writer(open(fn,"wb"))
    rows = []
    rows.append(['headline','project','found_release_number','problem_description'])
    rows.append([data['headline'],data['project'],data['found_release_number'],data['problem_description']])
    rows = [[e.encode('GBK') for e in row] for row in rows]
    writer.writerows(rows)


def parse_new_mr_ret(retStr):
    s = ''
    lines = retStr.splitlines()
    for line in lines:
        if line.find('error') > 0:
            s = line
            return False,s
    s = lines[0]
    return True,s
 
from workflow.settings import get_mssql_conn
def get_mr_id(dbid):
    mr_id = ''
    current_db = "HZ_ONSudb"
    current_server = 'HZ_RD_CSE'
    
    ms_conn=get_mssql_conn(current_db,current_server)
    
    if dbid:
        ms_cur = ms_conn.cursor()
        #直接查询表ProductSchema.dev_defect
        query="SELECT id FROM ProductSchema.dev_defect where dbid='%s'" % dbid 
        ms_cur.execute(query)
        mr_id=ms_cur.fetchone()
    mr_id = mr_id[0]
    ms_conn.close()
    return mr_id
        
    

from workflow.flow.cclock.views import get_user_email 
from workflow.settings import ONS_DATABASE_SET
from workflow.flow.cclock.views import MR_INFO
def edit(request):
    form =  CQNewMRForm()
    user_id = str(request.user)
    user_email = get_user_email(user_id)
    user_name = user_email[0:user_email.find('@')]
    user_name = user_name.replace(".","_")
    database_set = ONS_DATABASE_SET
    if request.POST:
        data = request.POST.copy()
        form = CQNewMRForm(data)
        if form.is_valid():
            succ = False
            from datetime import datetime
            fn = 'e:/tmp_newmr_csv/%s.csv' % datetime.now().microsecond
            new_mr_info2csv(fn,form.cleaned_data)
            import subprocess
            cmd = New_MR_CMD % (request.POST['cq_username'], \
                    'ONS',database_set,fn)
            p=subprocess.Popen(cmd, cwd=PERL_SCRIPT_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()
            rets = p.communicate()
            ret = rets[0].strip() + rets[1].strip()
            ret = ret.strip()
            t_err,dbid= parse_new_mr_ret(ret);
            if t_err:
                MR_INFO['mr_id'] = get_mr_id(dbid)
                MR_INFO['title'] = data['headline']
                MR_INFO['descn'] = data['problem_description']
                return HttpResponseRedirect('../cclock/my/newFlow2newMR')
            else:
                request.user.message_set.create(message=u"新建MR失败，失败在:" + dbid)
        else:
            request.user.message_set.create(message=u"输入数据有误")
    return render_to_response('mr_flow\mr_edit.html', \
            {'title':u'新建一个MR',\
            'user_name':user_name, \
            'form':form}, \
            context_instance=template.RequestContext(request))

def query(request):
    return HttpResponse(u'暂不支持此功能')



