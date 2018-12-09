#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/17 16:10
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : UserAuthMiddleware.py
# @Software: pycharm

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils.deprecation import MiddlewareMixin

from user.models import User


class UserMiddleware(MiddlewareMixin):
    # 重构拦截请求的方法
    def process_request(self, request):

        # 排除不需要登录验证的地址
        not_login_path = ['/user/register/', '/user/login/', ]
        path = request.path
        # 校验不需要登录验证的地址
        for n_path in not_login_path:
            # 如果当前访问的地址为登录地址或者注册地址，则直接访问对应的视图函数
            if path == n_path:
                return None
        try:
            # 获取session中已保存的user_id值
            username = request.session['username']
        except:
            # 跳转到登陆
            return HttpResponseRedirect(reverse('user:login'))
        # 根据这个id去数据库中查找对应的管理员
        user = User.objects.get(username=username)
        request.user = user
        return None

# def is_login(func):
#     def check(request):
#         try:
#             # 获取session中已保存的user_id值
#             request.session['user_id']
#         except:
#             # 跳转到登陆
#             return HttpResponseRedirect(reverse('user:login'))
#         return func(request)
#
#     return check
