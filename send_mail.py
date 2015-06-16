import smtplib
import socket
import string

from settings import  EMAIL_HOST,SERVER_EMAIL 
import sys  
import time  
import MySQLdb  
  
reload(sys)   
sys.setdefaultencoding('utf8')  

class CachedDnsName(object):
    def __str__(self):
        return self.get_fqdn()

    def get_fqdn(self):
        if not hasattr(self, '_fqdn'):
            self._fqdn = socket.getfqdn()
        return self._fqdn

DNS_NAME = CachedDnsName()

def send_mail(subject,message,email):
    connection = smtplib.SMTP(EMAIL_HOST,25, local_hostname=DNS_NAME.get_fqdn())
    email_info = string.join(("From:%s" % SERVER_EMAIL,
        "To:%s" % email,
        "Subject:%s" % subject,
        "",
        message),"\r\n")
#    print email_info
#    print EMAIL_HOST
#    print SERVER_EMAIL
    connection.sendmail(SERVER_EMAIL,email,email_info)
    connection.quit()

#send_mail("Hello","hello python","smwu@utstar.com")
