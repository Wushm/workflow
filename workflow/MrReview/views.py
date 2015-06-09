# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from workflow.MrReview.forms import ReviewForm,QueryForm
from workflow.MrReview.models import Review
from workflow.flow.cclock.models import MR, CCLockFlow
from workflow.settings import jobnumber_name, reviewer1_choices, reviewer2_choices, energy_choices, totaltime_choices, rootcase_choices, leadinto_choices, module_choices, team_choices

import re

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

@login_required
def add(request, id):
    """
    添加review信息
    """
    
    review_record = Review.objects.filter(workflow_id=id)
    if review_record:
        return HttpResponse("review信息已经添加，请返回并刷新页面！")
    
    data = {}
    mrs_submitter = {}
    
    cclock = CCLockFlow.objects.get(id=id)
    data['workflow_id'] = int(id)
    if jobnumber_name.has_key(cclock.submitter.username):
        data['submitter'] = jobnumber_name[cclock.submitter.username][0]
        data['team'] = jobnumber_name[cclock.submitter.username][1]
    else:
        data['submitter'] = cclock.submitter.username
        data['team'] = ""

    buglist = cclock.bugs.all()
    bugStr = ""
    for i in range(0, len(buglist)):
        if i > 0 :
            bugStr +=  " , "      
        bugStr += buglist[i].mr_id
    data['mrs'] = bugStr
    
    mrs_submitter['submitter'] = data['submitter']
    mrs_submitter['mrs'] = data['mrs']
    mrs_submitter['team'] = data['team']
    
    form = ReviewForm(data)

    if request.POST:
        data=request.POST.copy()
        form = ReviewForm(data)
        print form.is_valid()
        
        if form.is_valid():
            form.save()
            response = HttpResponse()
            response.__setitem__("Cache-control","no-cache");
            response.write("<script>history.go(-2);</script><p>成功添加MR review信息！</p>")
            return response
        else:
            return HttpResponse("添加MR review信息失败！")
    else:        
        return render_to_response('MrReview/mrReview_add.html', \
                {'title': u'MR review', 'form':form, 'mrs_submitter':mrs_submitter},  \
            context_instance=template.RequestContext(request))

def update(request, id):
    """
    更新
    """    
    form = ReviewForm()
    review_record = Review.objects.filter(workflow_id=id)
    review_record = review_record[0]
    
    if request.POST:
        data = request.POST.copy()
        review_record.submitter = data['submitter']
        review_record.reviewer1 = data['reviewer1']
        review_record.reviewer2 = data['reviewer2']
        review_record.reviewer3 = data['reviewer3']
        review_record.reviewer2_energy = data['reviewer2_energy']
        review_record.reviewer3_energy = data['reviewer3_energy']
        review_record.totalTime = data['totalTime']
        review_record.mrRootCause = data['mrRootCause']
        review_record.isLeadInto = data['isLeadInto']
        review_record.module = data['module']
        review_record.team = data['team']
        review_record.reasonDecription = data['reasonDecription']
        review_record.risk = data['risk']
        review_record.questionNum = data['questionNum']
        review_record.questionDecr = data['questionDecr']
        
        review_record.save()
        response = HttpResponse()
        response.__setitem__("Cache-control","no-cache");
        response.write("<script>history.go(-2);</script><p>成功修改MR review信息！</p>")
        return response
    
    return render_to_response('MrReview/mrReview_update.html', \
        {'title': u'MR Review 改动电子流', 
             'form': form,
             'review_record': review_record}, \
        context_instance=template.RequestContext(request))


def view(request,id):
    reviewinfo = Review.objects.filter(workflow_id=id)
    return render_to_response('MrReview/mrReview_view.html', \
            {'original': reviewinfo[0]}, \
        context_instance=template.RequestContext(request))
    
def query(request):
    form = QueryForm()
    t_err = 0
    review_records = Review.objects.all()
    if request.POST:
        data=request.POST.copy()
        submitter_name = data['submitter_name'].strip()
        mr_id = data['mr_id'].strip()
        approver_time = data['approver_time'].strip()
        if approver_time:
            t_err = error_msg(approver_time)
        reviewer_one = data['reviewer_one']
        reviewer_two = data['reviewer_two']
        mr_rootcause = data['mr_rootcause']
        mr_module = data['mr_module']
        team_name = data['team_name']
        
        if t_err:#如果遇到异常，设置错误信息
            form.is_valid()
            form.errors.ext_bugs = '<ul class="errorlist"><li>%s</li></ul>' % t_err
        else:
            if len(submitter_name) != 0:
                review_records = review_records.filter(submitter = submitter_name)
            if len(mr_id) != 0:
                review_records = review_records.filter(mrs__contains = mr_id)
            if len(approver_time) != 0:
                review_records = review_records.filter(reviewTime = approver_time)
            if len(reviewer_one) != 0:
                review_records = review_records.filter(reviewer1 = reviewer_one)
            if len(reviewer_two) != 0:
                review_records = review_records.filter(reviewer2 = reviewer_two)
            if len(mr_rootcause) != 0:
                review_records = review_records.filter(mrRootCause = mr_rootcause)
            if len(mr_module) != 0:
                review_records = review_records.filter(module = mr_module)
            if len(team_name) != 0:
                review_records = review_records.filter(team = team_name)
            
            table_head_list = []
            table_data_list = []
            review_result_list = request.REQUEST.getlist('review_result')
            for value in review_result_list:
                table_name = re.split(':', value)
                table_head_list.append(table_name[0])
                table_data_list.append(table_name[1])
    
            return render_to_response('MrReview/todo_mrreview.html', \
                    {'title': u'review 信息电子流', 'review_records': review_records.order_by('-reviewTime'), \
                    'table_head_list':table_head_list, 'table_data_list': table_data_list}, \
                context_instance=template.RequestContext(request))
        
    return render_to_response('MrReview/mrReview_query.html', \
            {'form':form}, \
        context_instance=template.RequestContext(request))
    
