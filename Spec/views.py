# Create your views here.
# -*- coding: UTF-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django import template
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import simplejson

from workflow.Spec.forms import SpecIdForm, QueryForm
from workflow.Spec.models import SpecIdApplyInfo
from workflow.settings import specId_choices,branch_choices,jobnumber_name

import re
import os
import sys

branch_dic = {
    "tn735"            : r"\\hz_rd_server\Code\Bamboo_735\OnsPlatform",
    "uniform"          : r"\\hz_rd_server\Code\Bamboo_Uniform\OnsPlatform",
    #"sbb_main"         : r"\\hz_rd_server\Code\Bamboo_SBB_1_2_0_DEV\OnsPlatform",
    "sbb_maintain"     : r"\\hz_rd_server\Code\Bamboo_765\OnsPlatform",
    #"sbb_18base"       : r'',
    #"uniform_maintain" : r"\\hz_rd_server\Code\Bamboo_Uni_Maintain\OnsPlatform",
    "sbb_r15"          : r"\\hz_rd_server\Code\Bamboo_SBB_705\OnsPlatform",
    #"701maintain"      : r'\\hz_rd_server\Code\Bamboo_701maintain\OnsPlatform',
    #"uniform_cht"      : r"\\hz_rd_server\Code\Bamboo_Uni_2_2_3\OnsPlatform",
}


def find_id_each_branch(dir, file_key, file_list, file_id_list):
	id_list = []
	find = 0
		
	for element in os.listdir(dir):
		fullpath = dir + r'/' + element
		if os.path.isdir(fullpath):
		    find_id_each_branch(fullpath, file_key, file_list, file_id_list)
		elif os.path.isfile(fullpath):
			m = re.match(file_key, element)
			if m is None:
			     continue

			num_list = re.split('\.', element)
			if (len(num_list) > 3) or (cmp(num_list[-1], 'td') != 0): 
				continue
			
			for file in file_list:
				if cmp(file, element) == 0:
					find = 1
					break
			
			if find:
			     continue
			
			file_list.append(element)
			
			#id_list = []
			maxId = 0
			f = open(fullpath, 'r')
			for eachline in f.readlines():
				value = re.findall('val="(\d+)"', eachline)
				if value != []:
					#for num in value:
					if int(value[0]) > maxId:
					    maxId = int(value[0])
					#id_list.append(int(value[0]))
	
			f.close()
			#id_list.sort()
			#file_id_list.append(id_list[-1])
			file_id_list.append(maxId)
			print file_list, file_id_list
	
	file_id_list.sort()
	if file_id_list != []:
		return file_id_list[-1]
	else:
		return 0
	

def find_ndt_tid(dir):
	tid_list = []
	find = False
	
	for element in os.listdir(dir):
		fullpath = dir + r'/' + element
		if os.path.isfile(fullpath):
			if re.search('otw$', element) is not None:
			    find = True
			    #print element
			    break
	
	if find:		
	    f = open(fullpath, 'r')
	    for eachline in f.readlines():
		m = re.search('\.xml', eachline)
		if m is not None:
		    fullpath = dir + r'/' + eachline.strip("\r\n")

		    f_xml = open(fullpath, 'r')
		    for eachline_xml in f_xml.readlines():
			value = re.findall('typeid="(\d+)"\s+size', eachline_xml)
			if value != [] and int(value[0]) > 0:
			    tid_list.append(int(value[0]))
	
		    f_xml.close()

	    f.close()

	tid_list.sort()
	#print tid_list
	
	if tid_list != []:
		return tid_list[-1]
	else:
		return 0

	
def find_max_id(file_key):
	max_id_list = []
	flag = 0
	ret = 0
	val = 0
	max_id = 0
	
	#建立与 hz_rd_server 的连接
	#ret = os.system(r'net use \\hz_rd_server\Code "WithMe07" /user:"hz07706"')

	if cmp(file_key, 'NDT') == 0:
		flag = 1
	else:
		file_key = '^' + file_key

	for key in branch_dic.keys():
		dir = re.sub(r'\\', '/', branch_dic[key])
		if flag:
			dir = dir + r'/xmllib'
		else:
			dir = dir + r'/spec'
		
		if os.path.exists(dir) == False:
			continue
		print dir
		#更新CC
		#os.system(r'cleartool update ' + dir)
		file_id_list = []
		if flag:
			id = find_ndt_tid(dir)
		else:
			file_list = []
			id = find_id_each_branch(dir, file_key, file_list, file_id_list)
		
		#max_id_list.append(id)
		if id > max_id:
			max_id = id
	"""	
	if max_id_list != []:
		max_id_list.sort()
		print max_id_list
		val = max_id_list[-1]
    """
	
	#删除连接	
	#if ret == 0:
	#    os.system(r'net use \\hz_rd_server\Code /del')

	#return val
	return max_id

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

def add(request):
    if jobnumber_name.has_key(str(request.user)):
        submitter = jobnumber_name[str(request.user)][0]
    else:
        submitter = request.user
        
    data = {}
    data['submitter'] = submitter
    data['maxId'] = 1
    form = SpecIdForm(data)
    
    if request.POST:
        data = request.POST.copy()
        db_max_val = 1
        max_val = 1
        specid_file = data['specIdFile']

        specid_record_set = SpecIdApplyInfo.objects.filter(specIdFile = specid_file).order_by('-maxId')
        if (specid_record_set):
            specid_record = specid_record_set[0]
            db_max_val = specid_record.maxId
            print "db max val is " + str(db_max_val)
            
        cc_max_val = find_max_id(specid_file)
        print "cc max val is " + str(cc_max_val)
        
        if(cc_max_val > db_max_val):
            max_val = cc_max_val
        else:
            max_val = db_max_val
            
        data['maxId'] = max_val + int(data['idNumbers'])
        
        form = SpecIdForm(data)
        print form.is_valid()

        if form.is_valid():
            form.save()
            if int(data['idNumbers']) == 1:
                return HttpResponse("申请"+str(data['specIdFile'])+" Id成功, id为" + str(max_val+1))
            elif int(data['idNumbers']) > 1:
                return HttpResponse("申请"+str(data['specIdFile'])+" Id成功, id为" + str(max_val+1) + " ~ " + str(data['maxId']))
        else:
            return HttpResponse("申请Spec Id失败！")
    return render_to_response('Spec/spec_add.html', \
                              {'title': u'Apply for Spec Id', 'form':form, 'submitter':submitter},  \
                              context_instance=template.RequestContext(request))

def query(request):
    form = QueryForm()
    t_err = 0
    t_err1 = 0
    spec_records = SpecIdApplyInfo.objects.all()
    
    if request.POST:
        data=request.POST.copy()
        submitter_name = data['submitter_name'].strip()
        specIdFile = data['specIdFile'].strip()
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
                spec_records = spec_records.filter(submitter = submitter_name)
            if len(specIdFile) != 0:
                spec_records = spec_records.filter(specIdFile = specIdFile)
            if len(submitTime_start) != 0:
                spec_records = spec_records.filter(submitTime__gte = submitTime_start)
                spec_records = spec_records.filter(submitTime__lte = submitTime_end)
            
            return render_to_response('Spec/todo_spec.html', \
                    {'title': u'规格电子流', 'spec_records': spec_records.order_by('-submitTime', '-maxId')},\
                    context_instance=template.RequestContext(request))
            
    return render_to_response('Spec/spec_query.html', \
            {'form':form}, \
        context_instance=template.RequestContext(request))
