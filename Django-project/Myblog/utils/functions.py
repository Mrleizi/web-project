#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/18 15:01
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : functions.py
# @Software: pycharm

from django.http import HttpResponseRedirect
from django.urls import reverse


def is_login(func):
    def check(request):
        try:
            # 获取session中已保存的user_id值
            request.session['user_id']
        except:
            # 跳转到登陆
            return HttpResponseRedirect(reverse('user:login'))
        return func(request)

    return check
