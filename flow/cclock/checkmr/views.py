# Create your views here.
# coding: utf-8
from django.shortcuts import render_to_response
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from workflow.flow.cclock.checkmr.forms import SearchMRForm, UpdateMRForm
from workflow.settings import get_mssql_conn
from workflow import settings
from django.http import HttpResponseRedirect

def _str2datetime(value, default_value):
    import datetime
    import time
    format='%Y-%m-%d %H:%M:%S'
    #value='2005-10-20 23:59:59'
    try:
        return datetime.datetime(*time.strptime(value, format)[:6])
    except:
        return default_value

def _format_start_end_date(start, end):
    """
    格式化开始/结束时间
    """
    from datetime import datetime
    start_date=datetime(1990,1,1)
    end_date=datetime(2099,1,1)
    if start:
        start_date = _str2datetime(start + ' 00:01:01', start_date)
    if end:
        end_date = _str2datetime(end + ' 23:59:59', end_date)
    return start_date, end_date

def _get_flow_descn(mr_id):
    """查询出修改了MR的flow"""
    from django.db import connection
    sql = """SELECT title, u.username, approve_time
FROM cclock_cclockflow flow, cclock_cclockflow_bugs f_m, auth_user u
WHERE flow.id = f_m.cclockflow_id
AND f_m.mr_id = %s
AND u.id = flow.submitter_id"""
    cursor = connection.cursor()#dict?
    cursor.execute(sql, (mr_id,))
    t_flows = cursor.fetchall()
    flow_descn = "<br/>".join(["%s/%s/%s" % (e[0],e[1],e[2],) for e in t_flows])
    return flow_descn

#TODO 缺少一个状态类型
_query_mr_sql ="""select distinct(mr.mr_id) from 
cclock_mr mr, cclock_cclockflow flow, cclock_cclockflow_bugs f_m where 
    mr.mr_id=f_m.mr_id 
    and flow.id=f_m.cclockflow_id 
    and flow.approve_result='o'
    and flow.approve_time>=%s
    and flow.approve_time<=%s"""
   
def _get_mr_infos(t_mrs, state):
    """
    重MSSQL中查询出MR信息
    """
    #'ONS00000058','ONS00000059'
    sql = "select id, headline, state_name from dbo.Dev_Projects_MR_Info where id in (%s) "
    mr_ids = ",".join(["'%s'" % e[0] for e in t_mrs])
    if not mr_ids:#如果不包含任何记录直接返回空
        return []
    sql = sql % mr_ids
    if state:
        sql = sql + " and state_name='%s'" % state
    ms_conn=get_mssql_conn()
    ms_cur = ms_conn.cursor()
    ms_cur.execute(sql)
    mrs=ms_cur.fetchall()
    ms_conn.close()
    return mrs

def index(request):
    """
    列出在指定时间段内修改的MR
    MR_ID 申请信息（title/submitter/date）
    """
    form = SearchMRForm(request.GET)
    uform = UpdateMRForm()
    if request.POST:
        """
        如果提交post请求，修改请求的状态
        调用perl脚本，批量修改状态
        """
        uform = UpdateMRForm(request.POST)#由于存在重定向，无法保存CQ表单信息
        import subprocess
        cmd = settings.Update_MR_CMD % (request.POST['cq_username'], \
                request.POST['cq_pswd'], 'ONS', " ".join(request.POST.getlist('selected_mr')))
        p=subprocess.Popen(cmd, cwd=settings.PERL_SCRIPT_DIR, stdout=subprocess.PIPE)    
        p.wait()
        ret = p.communicate()[0].strip()
        if "== create session fail ==" == ret:
            #return HttpResponse("用户名或密码不正确，无法连接Clear Quest");
            request.user.message_set.create(message=u"用户名或密码不正确，无法连接Clear Quest")
        else:
            request.user.message_set.create(message=u"更新成功")
        return HttpResponseRedirect('')#直接返回当前url
    from django.db import connection
    cursor = connection.cursor()#dict?
    from datetime import datetime
    params = _format_start_end_date(request.GET.get('start_date', ''), \
            request.GET.get('end_date', ''))
    cursor.execute(_query_mr_sql, params)
    t_mrs = cursor.fetchall()
    t_mrs = _get_mr_infos(t_mrs, request.GET.get('state', ''))
    mrs = []
    for t_mr in t_mrs:
        mr = {'id': t_mr[0], 'headline': t_mr[1].decode("GBK"), 'state': t_mr[2]}#TODO 当前状态，只显示状态不对的MR？
        mr['flow'] = _get_flow_descn(t_mr[0])
        mrs.append(mr)
    return render_to_response('cclock/checkmr/index.html', \
            {'title': u'ClearCase Lock 改动电子流', 'form':form, 'uform':uform, 'mrs':mrs}, \
        context_instance=template.RequestContext(request))
