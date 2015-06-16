import smtplib
import socket

class CachedDnsName(object):
    def __str__(self):
        return self.get_fqdn()

    def get_fqdn(self):
        if not hasattr(self, '_fqdn'):
            self._fqdn = socket.getfqdn()
        return self._fqdn

port = 25
host = 'loaclhost'
DNS_NAME = CachedDnsName()
local_hostname = DNS_NAME.get_fqdn()
print local_hostname

smtp = smtplib.SMTP(host,port,None)
smtp.login(None,None)
