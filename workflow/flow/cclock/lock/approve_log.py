#!/usr/bin/env python
# coding: utf-8
# don't delete line 2, important!
# copyright UTstarcom, ONS, platform team, 2006
from workflow.flow.cclock.lock import clearlock
from workflow.flow.cclock.lock.models import ApproveList, ApproveLog
from datetime import *
from workflow.settings import logging

def logAssign(eid,vobbranch) :
    eid = eid.lower()
    approveLog = ApproveList(EID=eid, ApproveTime=datetime.now(),
                VOBBranch=vobbranch, RecoverFlag=False)
    approveLog.save()
    approveLog = ApproveLog(OpTime=datetime.now(), EID=eid,
                OpType='assign', VOBBranch=vobbranch, IP="none")
    approveLog.save()

def logRecover(eid,vobbranch,auto_recover) :
    eid = eid.lower()
    if auto_recover :
        op_type = 'auto-recover'
    else :
        op_type = 'recover'
    approveLog = ApproveLog(OpTime=datetime.now(), EID=eid,
                OpType=op_type, VOBBranch=vobbranch, IP="none")
    approveLog.save()

def recoverApprove() :  # called every 20 minutes.
    print ApproveList.objects.all()
    logging.debug('== recoverApprove ==')
    allMustRecovered = ApproveList.objects.filter(ApproveTime__lte=datetime.now()
                    - timedelta(hours=12))
    for log in allMustRecovered :  # 查找所有权限到期用户
        print log
        try:
            users = clearlock.getLockExceptUsers(log.VOBBranch) # find all except users
            recoverFlag = True   # 如果用户不在 except users 列表, 也要删除log
            #FIXME 可能未能正确查询出lockusers
            if (users.find(log.EID) > -1) :  # 在列表中则回收权限, 并删除log
                logging.debug('[EID, users]' + log.EID + ' | ' + users)
                users = users.replace(log.EID,'')
                users = users.replace(',,', ',')
                users = users.strip(',')
                (lock_str,ret_code) = clearlock.replace_lock(log.VOBBranch,users)
                logging.debug('[users, VOBBranch, lock_str, ret_code]' + \
                        users + ' | ' + log.VOBBranch + ' | ' + lock_str + ' | ' + ret_code)
                # 回收 CCLock 权限
                if ret_code!='0' :  # 如果命令没有执行成功, 则不删除该 log
                    recoverFlag = False
            if recoverFlag:#记录回收日志
                logRecover(log.EID,log.VOBBranch,True)
                log.RecoverFlag = recoverFlag
                log.save()
        except:
            pass
    allRecovered = ApproveList.objects.filter(RecoverFlag = True)
    allRecovered.delete()

if __name__ == "__main__":
    # logApprove('hz084945','none2')
    # p = ApproveList.objects.all()[0]
    # to-do 剩下回收权限和tt整合
    # print p.EID
    recoverApprove()  # 计划任务每 20 分钟检查一次;
