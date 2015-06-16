#coding:utf-8

import urllib,urllib2,cookielib
import socks
from HTMLParser import HTMLParser
import sys

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    isTable = False
    isMyData = False
    dataNumber = 0
    userInfo = {}
    def __init__(self):
        HTMLParser.__init__(self)
        self.isTable = False
        self.isMyData = False
        self.dataNumber = 0
        self.userInfo = {'e_name':'','c_name':'','email':''}
        
    def handle_starttag(self, tag, attrs):
        if tag == "table":
            #print "Encountered a start attrs:",attrs 
            for i in range(len(attrs)):
                #print "attr:\n",attrs[i]
                if attrs[i][0] == 'bordercolor' and attrs[i][1] == '#DADADA':
                     self.isTable = True
                     return 
        if self.isTable and tag == 'a':
            if len(attrs) ==0:
                pass
            else:
                if attrs[0][0] == 'href' and attrs[0][1] == '#':
                    self.isMyData = True
        if self.isTable and self.isMyData and tag == 'td':
            self.dataNumber = self.dataNumber + 1   
                    
                
    def handle_endtag(self, tag):
        if tag == "table":
            #print "Encountered an end tag :", tag
            self.isTable = False
            self.isMyData = False
    def handle_data(self, data):
        if self.isMyData:
            if self.dataNumber == 3:
                self.userInfo['e_name'] = self.userInfo['e_name'] + data
            if self.dataNumber == 4:
                self.userInfo['c_name'] = self.userInfo['c_name']  + data.decode('gbk').encode('utf-8')
            if self.dataNumber == 7:
                self.userInfo['email'] = self.userInfo['email'] + data


def get_user_info(user_number):
    #创建Opener----------------------------
    #创建cookie对象
    cookie = cookielib.CookieJar()

    #创建COOKIE处理程序
    cookieProc = urllib2.HTTPCookieProcessor(cookie)

    #创建opener
    opener = urllib2.build_opener(cookieProc)

    #安装到urlopen()(这里也可以不用install_opener)
    urllib2.install_opener(opener)

    #发起请求------------------------------
    tmp_url='http://home.utstar.com.cn/it/search/default.asp?gen=&uid=' + user_number + '&Submit=%B2%E9%D1%AF'

    #Request
    req = urllib2.Request(
            url = tmp_url,
            )
    res = None
    #请求
    try:
        res = urllib2.urlopen(req).read()
    except:
        return None
    parser = MyHTMLParser()
    parser.feed(res)
    parser.close()
    user_info = parser.userInfo
    return user_info


#user_info = get_user_info('hz05999')
#print user_info
