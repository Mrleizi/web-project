#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/25 10:31
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : forms.py
# @Software: pycharm

from django import forms


class UserLoginForm(forms.Form):
    username = forms.CharField(required=True,
                               error_messages={'required': '账号必填'})

    password = forms.CharField(required=True,
                               error_messages={'required': '密码必填'})
