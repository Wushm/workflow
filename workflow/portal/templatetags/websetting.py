from django.template import Library
from workflow import settings

register = Library()

def get_setting_value(key):
    """
    try:
        from django.conf import settings
    except ImportError:
        return ''"""
    if 'SITE_NAME'==key:
        return settings.SITE_NAME
    if 'URL_PREFIX'==key:
        return settings.URL_PREFIX
    if 'URL_PREFIX_'==key:
        return settings.URL_PREFIX_
    return ''

def site_name():
    return get_setting_value('SITE_NAME')

def url_prefix():
    return get_setting_value('URL_PREFIX')

def url_prefix_():
    return get_setting_value('URL_PREFIX_')

site_name = register.simple_tag(site_name)
url_prefix = register.simple_tag(url_prefix)
url_prefix_ = register.simple_tag(url_prefix)
