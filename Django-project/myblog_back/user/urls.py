#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/12/4 19:53
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter, SimpleRouter

from user import views

# 引入路由
# router = DefaultRouter()
# router = SimpleRouter()
# 使用router的地址
# router.register(r'users', views.UserView)
# router.register(r'login2', views.UserLoginView, base_name='login2')

urlpatterns = [
    # 注册
    url(r'^register/', views.register, name='register'),
    # 登录
    url(r'^login/', views.login, name='login'),
    # 首页
    url(r'^index/', views.index, name='index'),
    # 退出登录
    url(r'^logout/', views.logout, name='logout'),
    # 个人信息
    url(r'^personal_details/', views.personal_details, name='personal_details'),
    # 公告
    url(r'^notice/', views.notice, name='notice'),
    # 增加公告
    url(r'^add_notice/', views.add_notice, name='add_notice'),
    # 删除公告
    url(r'^delete_notice/', views.delete_notice, name='delete_notice'),
    # 友情链接
    url(r'^flink/', views.flink, name='flink'),
    # 添加友情链接
    url(r'^add_flink/', views.add_flink, name='add_flink'),
    # 修改友情链接
    url(r'^update_flink/(\d+)/', views.update_flink, name='update_flink'),
    # 删除友情链接
    url(r'^delete_flink/', views.delete_flink, name='delete_flink'),
    # 登录记录
    url(r'^loginlog/', views.loginlog, name='loginlog'),
    # 删除登录记录
    url(r'^delete_loginlog/', views.delete_loginlog, name='delete_loginlog'),
    # 清除本人登录记录
    url(r'^delete_uloginlog/', views.delete_uloginlog, name='delete_uloginlog'),
    # 清除所有登录记录
    url(r'^delete_aloginlog/', views.delete_aloginlog, name='delete_aloginlog'),
    # 管理用户
    url(r'^manage_user/', views.manage_user, name='manage_user'),
    # 基本设置
    url(r'^setting/', views.setting, name='setting'),
    # 阅读设置
    url(r'^readset/', views.readset, name='readset'),
    # 删除用户
    url(r'^delete_user/', views.delete_user, name='delete_user')

]
# urlpatterns += router.urls
# urlpatterns = format_suffix_patterns(urlpatterns)
