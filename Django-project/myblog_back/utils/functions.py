#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/18 15:01
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : functions.py
# @Software: pycharm

from django.http import HttpResponseRedirect
from django.urls import reverse

from user.models import User


def is_login(func):
    def check(request, *args, **kwargs):
        # 获取session中已保存的user_id值
        username = request.session.get('username')
        if username:
            user = User.objects.get(username=username)
            request.user = user
            return func(request, *args, **kwargs)
        return HttpResponseRedirect(reverse('user:login'))

    return check
