#!/usr/bin/env python
# -*-coding:UTF-8-*-#
from MySQLdb import Connection
from settings import *
from ut.common.db_utils import *

def get_discuz_db_conn():
    """
    获取discuz的数据库连接
    """
    return Connection(DISCUZ_DATABASE_HOST, DISCUZ_DATABASE_USER, \
            DISCUZ_DATABASE_PASSWORD, DISCUZ_DATABASE_NAME, \
            charset=DISCUZ_CHARSET)

def dz_execute(sql, params=(), action=EXEC_UPDATE, curType='dict'):
    return execute(get_discuz_db_conn(), sql, params, action, True, \
        curType=curType)

#############################
def get_mydms_db_conn():
    """
    获取discuz的数据库连接
    """
    conn = Connection(MYDMS_DATABASE_HOST, MYDMS_DATABASE_USER, \
            MYDMS_DATABASE_PASSWORD, MYDMS_DATABASE_NAME, \
            charset=MYDMS_CHARSET)
    #execute(conn, "SET NAMES "+MYDMS_CHARSET, (), EXEC_UPDATE, False)
    return conn

def mydms_execute(sql, params=(), action=EXEC_UPDATE, curType='dict'):
    return execute(get_mydms_db_conn(), sql, params, action, True, \
        curType=curType)

if __name__=='__main__':
    pass
