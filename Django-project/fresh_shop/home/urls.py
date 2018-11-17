#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/28 19:17
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm


from django.conf.urls import url

from home import views

urlpatterns = [
    # 首页地址
    url(r'^index/', views.index, name='index'),
]
