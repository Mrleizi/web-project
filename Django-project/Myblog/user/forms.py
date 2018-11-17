#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/14 10:52
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : forms.py
# @Software: pycharm

"""
导入规则
1.新引入python自带的库

2.引入第三方库

3.引入自定义的
"""
from django import forms
from django.contrib.auth.models import User

from user.models import Admin, Article


class UserForm(forms.Form):
    """
    校验注册信息
    """
    name = forms.CharField(required=True, max_length=20, min_length=2,
                           error_messages={'required': '姓名必填',
                                           'max_length': '用户名不能超过12个字',
                                           'min_length': '用户名不能少于2个字'})
    username = forms.CharField(required=True, max_length=24, min_length=2,
                               error_messages={'required': '用户名必填',
                                               'max_length': '用户名不能超过8个字符',
                                               'min_length': '用户名不能少于2个字符'})
    tel = forms.CharField(required=False, max_length=11)

    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码必填',
                                               'min_length': '密码不能少于6个字符'})
    password2 = forms.CharField(required=True, min_length=6,
                                error_messages={'required': '确认密码必填',
                                                'min_length': '确认密码不能少于6个字符'})

    def clean(self):
        # 校验用户名是否已经注册过（进入数据库查找username）
        user = Admin.objects.filter(username=self.cleaned_data.get('username'))
        # user 为空就没人注册 <QuerySet [<User: admin>]>就有人注册
        if user:
            # 如果已经注册过
            raise forms.ValidationError({'username': '用户名已存在，请直接登录'})

        # 校验密码和确认密码是否相同
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError({'password': '两次密码不一致'})
        return self.cleaned_data  # 返回一个字典


class UserLoginForm(forms.Form):
    # 校验用户名和密码
    """定义类的字段username <django.forms.fields.CharField object at 0x000002B1BAFCE2B0>"""
    username = forms.CharField(required=True, max_length=24, min_length=2,
                               error_messages={'required': '用户名必填',
                                               'max_length': '用户名不能超过8个字符',
                                               'min_length': '用户名不能少于2个字符'},
                               )
    # 'min_length': '密码不能少于6个字符'
    """定义类的字段password <django.forms.fields.CharField object at 0x000002B1BAFCE2B0>"""
    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码必填',
                                               'min_length': '确认密码不能少于6个字符',
                                               })

    # 表单验证
    def clean(self):
        # 校验用户是否注册过(进入数据库)

        """用类中的字段username去数据库中校验"""
        # user = User.objects.filter(username=self.cleaned_data['username123'])
        """用从html获取的input的name='username' 去数据库中校验"""
        user = User.objects.filter(username=self.data['username'])
        # if not user:
        #     """把抛出的异常赋值给【类中】定义的username字段"""
        #     raise forms.ValidationError({'username': '用户名不存在,请先注册再来登录 '})
        return self.cleaned_data  # 返回一个字典


class AddArticle(forms.Form):
    # 文章验证
    title = forms.CharField(required=True, max_length=50)
    content = forms.CharField(widget=forms.Textarea)
    keywords = forms.CharField(required=True, max_length=50)
    describe = forms.CharField(widget=forms.Textarea)
    category = forms.CharField(required=True)
    tags = forms.CharField(required=True)
    titlepic = forms.ImageField(required=False)
    visibility = forms.CharField(required=True)
