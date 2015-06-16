#!/usr/bin/env python
# -*-coding:UTF-8-*-#
from MySQLdb import *
from settings import *
import MySQLdb

EXEC_UPDATE=0#return undated count.
EXEC_FETCHALL=1#return all rows.
EXEC_FETCHONE=2#return one row.
EXEC_INSERT=3#return last_insert_id.

def close_ig_exception(o):
    try:
        o.close()
    except:
        pass

def close_cur(cur, conn):
    close_ig_exception(cur)
    close_ig_exception(conn)

def get_insert_id(conn):
    return execute(conn, "SELECT last_insert_id()", (), EXEC_FETCHONE, False)['last_insert_id()']

def dj_get_first_sql_ret(sql, params=()):
    """
    Django的辅助工具类，获取的的一个查询值
    """
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute(sql, params)
    row = cursor.fetchone()
    count=row[0]
    return count

def execute(conn, sql, params=(), action=EXEC_UPDATE, close_conn=True, \
        curType='dict'):
    """
    执行SQL并返回执行结果
    action:
    EXEC_UPDATE=0#return undated count.
    EXEC_FETCHALL=1#return all rows.
    EXEC_FETCHONE=2#return one row.
    EXEC_INSERT=3#return last_insert_id.
    """
    if 'dict'==curType:
        cur=conn.cursor(MySQLdb.cursors.DictCursor)
    else:
        cur=conn.cursor()
    if params:
        cur.execute(sql, params)
    else:
        cur.execute(sql)
    if action==EXEC_UPDATE:
        ret=cur.rowcount
    if action==EXEC_FETCHONE:
        ret=cur.fetchone()
    if action==EXEC_FETCHALL:
        ret=cur.fetchall()
    if action==EXEC_INSERT:
        ret=get_insert_id(conn)
    if close_conn:
        close_cur(cur, conn)
    else:
        close_ig_exception(cur)
    return ret

if __name__=='__main__':
    pass
