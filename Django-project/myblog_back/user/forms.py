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
import re

from django import forms
from django.contrib.auth.hashers import check_password

from django.contrib.auth.models import User

from user.models import User


class UserForm(forms.Form):
    """
    校验注册信息
    """
    truename = forms.CharField(required=True, max_length=20, min_length=2,
                               error_messages={'required': '真实姓名必填',
                                               'max_length': '用户名不能超过12个字',
                                               'min_length': '用户名不能少于2个字'})
    username = forms.CharField(required=True, max_length=24, min_length=2,
                               error_messages={'required': '用户名必填',
                                               'max_length': '用户名不能超过8个字符',
                                               'min_length': '用户名不能少于2个字符'})
    usertel = forms.CharField(required=False, max_length=11)

    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码必填',
                                               'min_length': '密码不能少于6个字符'})
    password2 = forms.CharField(required=True, min_length=6,
                                error_messages={'required': '确认密码必填',
                                                'min_length': '确认密码不能少于6个字符'})

    def clean(self):
        # 校验用户名是否已经注册过（进入数据库查找username）
        user = User.objects.filter(username=self.cleaned_data.get('username'))
        # user 为空就没人注册 <QuerySet [<User: User>]>就有人注册
        if user:
            # 如果已经注册过
            raise forms.ValidationError({'username': '用户名已存在，请直接登录'})

        # 校验密码和确认密码是否相同
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError({'password': '两次密码不一致'})
        return self.cleaned_data  # 返回一个字典

    def clean_usertel(self):
        mobile = self.cleaned_data['usertel']
        if re.fullmatch(r'^1[34578]\d{9}$', mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码格式有误')


class UserLoginForm(forms.Form):
    """
    校验登录信息
    """
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
        user = User.objects.filter(username=self.cleaned_data['username']).first()
        if not user:
            #     """把抛出的异常赋值给【类中】定义的password字段"""
            raise forms.ValidationError({'password': '用户名或密码错误 '})

        if not check_password(self.cleaned_data['password'], user.password):
            raise forms.ValidationError({'password': '用户名或密码错误 '})

        return self.cleaned_data  # 返回一个字典


class UserUpdateForm(forms.Form):
    """
    校验注册信息
    """
    truename = forms.CharField(required=True, max_length=20, min_length=2,
                               error_messages={'required': '真实姓名必填',
                                               'max_length': '用户名不能超过12个字',
                                               'min_length': '用户名不能少于2个字'})
    username = forms.CharField(required=True, max_length=24, min_length=2,
                               error_messages={'required': '用户名必填',
                                               'max_length': '用户名不能超过8个字符',
                                               'min_length': '用户名不能少于2个字符'})
    usertel = forms.CharField(required=False, max_length=11)

    password = forms.CharField(required=True, min_length=6,
                               error_messages={'required': '密码必填',
                                               'min_length': '密码不能少于6个字符'})
    password2 = forms.CharField(required=True, min_length=6,
                                error_messages={'required': '确认密码必填',
                                                'min_length': '确认密码不能少于6个字符'})

    def clean(self):
        # 校验密码和确认密码是否相同
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError({'password': '两次密码不一致'})
        return self.cleaned_data  # 返回一个字典

    def clean_usertel(self):
        mobile = self.cleaned_data['usertel']
        if re.fullmatch(r'^1[34578]\d{9}$', mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码格式有误')


class NoticeForm(forms.Form):
    """公告校验"""
    title = forms.CharField(required=True, max_length=50)
    content = forms.Textarea()
    keywords = forms.CharField()
    describe = forms.CharField(widget=forms.Textarea)
    visibility = forms.CharField(required=True)


class FlinkForm(forms.Form):
    """友情链接"""
    name = forms.CharField(required=True)
    url = forms.CharField(required=True)
    imgurl = forms.CharField(required=True)
    describe = forms.CharField(widget=forms.Textarea)
    target = forms.IntegerField(required=True)
    rel = forms.IntegerField(required=True)
