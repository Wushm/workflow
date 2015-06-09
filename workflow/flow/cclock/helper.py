#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from workflow.settings import get_mssql_conn

def get_key_word(s):
    if s.find(':') == -1:
        return '', s
    pos = s.find(':')
    return s[:pos], s[pos+1:]

def get_mr_infos(mr_id):
    from workflow.settings import SBB_SERVER
    current_server = 'HZ_RD_CSE'
    try:
        if mr_id.find("BAN") > -1:
            current_db = "HZ_BANudb"
        elif mr_id.find("SBB") > -1:
            current_db = "SBBudb"
            current_server = SBB_SERVER
        else :
            current_db = "HZ_ONSudb"
    except:
        current_db = "HZ_ONSudb"
    ms_conn=get_mssql_conn(current_db,current_server)
    ms_cur = ms_conn.cursor()
    query="SELECT * FROM dbo.Dev_Projects_MR_Info where id='%s'" % mr_id
    ms_cur.execute(query)
    mr=ms_cur.fetchone()
    if not mr:
        query="SELECT * FROM dbo.Fld_Projects_MR_Info where id='%s'" % mr_id
        ms_cur.execute(query)
        mr=ms_cur.fetchone()            
    if not mr:
        query="SELECT * ProductSchema.dev_defect where id='%s'" % mr_id
        ms_cur.execute(query)
        mr=ms_cur.fetchone()            
    #print mr.id
    ms_conn.close()
    return mr

def decode_gbk(s):
    if s:
        return s.decode("GBK")
    return ''

def parse_cc_descn(descn):
    s=''
    key_words = ['MR', 'vob_branch_1', 'vob_branch_2', 'vob_branch_3', 'vob_branch_4', 'vob_branch_5', 'vob_branch_6','Modifiers', 'Problem caused', 'Resolution','Suggest Modules To Be Tested','Modified Files']
    helper_infos = []
    t_infos = {}
    lines = descn.splitlines()
    for line in lines:
        line = line.strip()
        if not line:
            continue
        key_word, content = get_key_word(line)
        if key_word in key_words:
            if line.startswith('MR:'):
                t_infos = {}
                helper_infos.append(t_infos)
                if content.find(' ') > 0:
                    content = content[0:content.find(' ')]
            t_infos[key_word] = content.strip()
    #TODO get mr infos
    infos = []
    for e in helper_infos:
        info = get_mr_infos(e['MR'])
        if not info:
            continue
        info = {'id': info.id, \
                'state_name': decode_gbk(info.state_name), \
                'introduction_phase': decode_gbk(info.introduction_phase), \
                'impacted_unit': decode_gbk(info.impacted_unit), \
                'load_information': decode_gbk(info.load_information), \
                'resolution_by': decode_gbk(info.resolution_by), \
                'problem_cause_by': decode_gbk(info.problem_cause_by), \
                'altered_file': decode_gbk(info.altered_file), \
                'headline':decode_gbk(info.headline),\
                'tests_executed_by': decode_gbk(info.tests_executed_by)}
        infos.append(info)
    return helper_infos, infos

def mr_infos2csv(fn, data):
    import csv
    writer = csv.writer(open(fn, "wb"))
    rows = []
    rows.append(['mr_id', 'reviewer', 'introduction_phase', 
            'impacted_unit', 'load_information', 
            'resolutin_by_assignee', 'problem_casued_by_assignee', 
            'files_altered_by_assignee', 'test_exeCuted_by_assignee'])
    rows.append([data['mr_id'], data['reviewer'], data['introduction_phase'], 
            data['impacted_unit'], data['load_information'], 
            data['resolutin_by_assignee'], data['problem_casued_by_assignee'], 
            data['files_altered_by_assignee'], data['test_exeCuted_by_assignee']])
    rows = [[e.encode('GBK') for e in row] for row in rows]
    writer.writerows(rows)
