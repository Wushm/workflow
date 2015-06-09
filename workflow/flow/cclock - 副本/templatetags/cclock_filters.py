#coding=utf-8
from django import template

register = template.Library()

def approve_result(value):
    #TODO 添加一个图像？
    if not value:
        return u'待审核'
    t=value[0]
    if t == 'o':
        return '批准'
    if t == 'x':
        return '驳回'
    return value
register.filter('approve_result', approve_result)

def str_bugs(bugs):
    bugs = [b.mr_id for b in bugs]
    return ",".join(bugs)
register.filter('str_bugs', str_bugs)

def attachments(value):
    def decode_filename(fn):
        import urllib
        fn = fn.encode('UTF-8')
        fn = urllib.unquote(fn)
        return fn.decode('UTF-8')
    """
    显示附件信息
    """
    #TODO 为附件增加图标
    #TODO 将update目录设置到web目录或者通过设置rewirter等方式让用户可以访问
    if not value:
        return ""
    #import urllib
    ss = value.splitlines()
    s = ""
    from workflow.settings import ATTACHMENTS_URL
    base_html = '<a href="%s">%s</a>' % (ATTACHMENTS_URL, '%s')
    atts = []
    for s in ss:
        org_filename, filename = s.strip().split('|')
        org_filename = decode_filename(org_filename)#urllib.unquote(org_filename)
        t_html = base_html % (filename, org_filename)
        atts.append(t_html)
    return ", ".join(atts)
register.filter('attachments', attachments)

def js_str(value):
    if value:
        return value.replace('\\', '\\\\')
    return value
register.filter('js_str', js_str)
