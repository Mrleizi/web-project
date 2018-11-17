#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/25 9:31
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from home import views

urlpatterns = [
    # 登录页面
    url(r'^login/', views.login, name='login'),
    # 首页
    url(r'^index/', login_required(views.index), name='index'),


    # 退出登录
    url(r'^logout/', views.logout, name='logout')
]
