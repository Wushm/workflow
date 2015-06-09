#coding=utf-8
from django import template
from workflow.settings import approvers as _approvers
from workflow.settings import approver_name as _approver_name
from django.utils import simplejson

register = template.Library()

def approvers():
    json = simplejson.dumps(_approvers, ensure_ascii = False) 
    return json
   
def approver_name():
    json = simplejson.dumps(_approver_name, ensure_ascii = False) 
    return json

approvers = register.simple_tag(approvers)
approver_name = register.simple_tag(approver_name)

approve_result_filters = (('', u'全部'), ('u', u'待审核'), ('x', u'驳回'), ('o', u'审核通过'))
class ApproveResultFilterNode(template.Node):
    def __init__(self):
        pass

    def render(self, context):
        q = ''
        try:
            q = context['q_approve_result']
        except:
            pass
        base_html = u'<a href="?q_approve_result=%s">%s</a>'
        htmls = []
        for e in approve_result_filters:
            t_html = base_html % e
            if q == e[0]:
                t_html = '<b>%s</b>' % t_html
            htmls.append(t_html)
        return " | ".join(htmls)

def do_approve_result_filter(parser, token):
    return ApproveResultFilterNode()

register.tag('approve_result_filter', do_approve_result_filter)
