# -*- coding: UTF-8 -*-
from django import newforms as forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=40, widget=forms.widgets.TextInput(\
        attrs={'style':'width: 10em;'}), label=u'登录名')
    password = forms.CharField(max_length=40, widget=forms.widgets.PasswordInput(\
        attrs={'style':'width: 10em;'}), label=u'密码')
    useremail = forms.CharField(max_length=40, widget=forms.widgets.TextInput(\
        attrs={'style':'width: 10em;'}), label=u'邮件')
