# -*- coding: UTF-8 -*-
DEBUG = True
TEMPLATE_DEBUG = DEBUG

import os
ROOT_DIR = os.path.dirname(__file__)
#UPLOAD_DIR = os.path.join(ROOT_DIR, 'upload')#上传文件位置
UPLOAD_DIR = r'E:\web\xampp\htdocs\workflow_upload'
PERL_SCRIPT_DIR = os.path.join(ROOT_DIR, 'perl_scripts')
Update_MR_CMD = 'cqperl UpdateMR.pl "%s" "%s" "%s" %s'#username pswd cq_db mrs.....
Rfb_MR_CMD = 'cqperl RfbMR.pl "%s" "%s" "%s" "%s"'#username pswd cq_db mrs.....
New_MR_CMD = 'cqperl submit_new_mr.pl "%s" "%s" "%s" "%s"'

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'mysql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = 'workflow'             # Or path to database file if using sqlite3.
DATABASE_USER = 'root'             # Not used with sqlite3.
DATABASE_PASSWORD = 'admin'         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.
#DATABASE_STORAGE_ENGINE = "MyISAM / INNODB / ETC"
DATABASE_OPTIONS = {"init_command": "SET foreign_key_checks = 0;"}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Asia/Shanghai PRC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'zh-cn'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = './static/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/workflow/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/django_admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 't#tz#_+5u1wkk$)dbirg*d5de-o9uh8pn#)r#hi1uro3=vja_a'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
)

ROOT_URLCONF = 'workflow.urls_prefix'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',

    'django.contrib.admin', 
    'workflow.flow.cclock',
    'workflow.flow.cclock.lock',
    'workflow.flow.cclock.checkmr',
    'workflow.portal',
    'workflow.mr_flow',
    'workflow.MrReview',
    'workflow.Spec',
    'workflow.addnewfile',
    'workflow.VobConfig'
)

############################################
#将api目录设置到环节目录中
EMAIL_HOST = "hzsmtp.utstar.com.cn"
#EMAIL_HOST = "CNMAIL13.cn.utstarcom.com"
#EMAIL_HOST_USER = 'UTSCN\hz05999'
#EMAIL_HOST_PASSWORD = 'UTpw201212'
SERVER_EMAIL = 'admin@utstar.com'

URL_PREFIX = 'workflow'#unicenter
URL_PREFIX_ = 'workflow/'#unicenter/
SITE_NAME = u'工作流'
LOGIN_URL = '/' + URL_PREFIX + '/login/'

BASE_URL = r'http://172.18.10.171/workflow'
CCLOCK_URL = BASE_URL + r'/cclock/my/%s/'
MR_MANAGE_URL = BASE_URL + r'/mr_manage'
APPROVE_CCLOCK_URL = BASE_URL + r'/cclock/todo/%s/'
DO_APPROVE_CCLOCK_URL = BASE_URL + r'/cclock/todo/%s/approve/'
ATTACHMENTS_URL = BASE_URL + r'_upload/%s'

SBB_SERVER = '172.21.150.35'

ONS_DATABASE_SET = "CQMS.UTSTARCOM.HZ"


def get_mssql_conn(db='HZ_ONSudb',Server='HZ_RD_CSE'):
    """
    import pymssql
    conn = pymssql.connect(host='HZ_RD_CSE',user='cse_reader',password='csereader',database=db)
    return conn
    """
    import pyodbc
    ms_conn = pyodbc.connect("DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=cse_reader;PWD=csereader" % (Server,db))#HZ_ONSudb
    return ms_conn

DISCUZ_TABLEPRE='cdb_'
def get_discuz_conn(db='HZ_ONSudb'):
    from MySQLdb import Connection
    return Connection('127.0.0.1', 'root', ' ', 'discuz', charset='utf8')

#导入uniceter的api，在使用完后再移除路径
unicenter_api_path = r'e:/web/xampp/django_project/unicenter'
def uncenter_auth(username, password):
    import subprocess
    cmd = 'python uc_api.py' + ' auth "%s" "%s" utscn' % (username, password)
    p=subprocess.Popen(['D:/Python25/python.exe', 'uc_api.py', 'auth', username, password, 'utscn'], cwd=unicenter_api_path, stdout=subprocess.PIPE)    
    # p.wait()
    ret = p.communicate()[0].strip()
    return "True" == ret

############ log ############
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s]%(levelname)-8s"%(message)s"',
                    datefmt='%Y-%m-%d %a %H:%M:%S',
                    filename=r'e:/workflow_log.log',
                    filemode='a+')

FIRST_LOGIN = True

try:
    from workflow.vob_config import *
except Exception, e:
    from vob_config import *
    

