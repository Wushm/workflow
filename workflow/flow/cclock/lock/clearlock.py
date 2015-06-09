#!/usr/bin/env python
# coding: utf-8
# don't delete line 2, important!
# copyright UTstarcom, ONS, platform team, 2006
import tempfile
import os
from subprocess import *
from workflow.settings import approve_servers, logging, vob_masters

def ls_lock(vobbranch) :
    logging.debug('== ls_lock ==')
    xfile = file(os.path.join(tempfile.gettempdir(), 'python_cclock_approve.txt'), 'w+')
    p1 = Popen(['onsrsh.exe', approve_servers[vobbranch], 'cleartool.exe','lsh','brtype:'+vobbranch],stdout=xfile)
    p1.wait()
    xfile.close()
    xfile = file(xfile.name)
    #lock_str = xfile.read().decode("mbcs").encode("utf8").splitlines()
    lock_str = xfile.read().decode("mbcs").splitlines()
    logging.debug('[vobbranch, lock_str]'+ vobbranch + ' | ' + str(lock_str) + ' | ' + approve_servers[vobbranch])
    xfile.close()
    #print "= lock_str =", lock_str
    del_line = 0
    for i in range(len(lock_str)) :
        if lock_str[i].find(' lock branch type ') == -1 : # 非 lock 记录行
            continue
        if lock_str[i].find("-2013") == -1 :
            del_line = i # 找出第一个非 2013 年 lock 记录行
            break
    del lock_str[0:del_line]  # 删除2013年操作记录, 如:  09-八月-2013 hzxxxx lock branch type "zzzz" (locked)
    last_lock = []  # 最新的 lock 记录
    for i in range(len(lock_str)):
        if lock_str[i].find(' lock branch type ') > -1 :
            last_lock.append(lock_str[i]) # lock 记录
            last_lock.append(lock_str[i+1]) # lock users
            break
    last_lock.append(str(p1.returncode)) # lock users
    logging.debug('[last_lock]' + str(last_lock))
    return last_lock

def add_master(vobbranch,users):
    # 检查特定用户是否在分支中，如果不在，则加上
    masters = []
    try:
        masters = vob_masters[vobbranch]
    except Exception, e:
        pass
    for u in masters:
        if not users.count(u):
            users += ',' + u
    users = users.strip(',')
    return users

def replace_lock(vobbranch,users):
    users = users.lower()
    users = add_master(vobbranch, users)
    xfile = file(os.path.join(tempfile.gettempdir(), 'python_cclock_approve.txt'), 'w+')
    params = ['onsrsh.exe', approve_servers[vobbranch],
         'cleartool.exe','lock','-replace']
    if users:
        params.extend(['-nusers',users])
    params.append('brtype:'+vobbranch)
    logging.debug('[replace_lock]' + str(params))
    p1 = Popen(params,stdout=xfile)
    p1.wait()
    xfile.close()
    xfile = open(xfile.name)
    return (xfile.read().decode("mbcs").encode("utf8"),str(p1.returncode))

def getLockExceptUsers(vobbranch):
    #这里可能会出现异常，外部想要进行异常处理
    last_lock = ls_lock(vobbranch)
    users = last_lock[1].replace('Locked except for users:','').replace('"','').strip()
    if users.find('all')>-1 :
        return ''
    users = users.replace(' ',',')
    return users.lower()

if __name__ == '__main__':
    vobbranch = '10G_CHT_06MAR30_BR@\NetRing'
    users = 'hz08678,hz08483'
    print add_master(vobbranch,users)
