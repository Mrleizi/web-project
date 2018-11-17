#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/28 19:19
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm

from django.conf.urls import url

from orders import views

urlpatterns = [
    # 本次订单中的商品信息
    url('^get_order_message/', views.get_order_message, name='get_order_message'),
    # 订单提交
    url(r'^order/', views.order, name='order'),
    # 查看全部订单
    url(r'^user_center_order/', views.user_center_order, name='user_center_order'),
    # 删除订单
    url(r'^delete_order_info/', views.delete_order_info, name='delete_order_info')
]
