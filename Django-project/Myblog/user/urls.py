#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/19 20:14
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm

from django.conf.urls import url

from user import views

urlpatterns = [
    # 访问前端的url
    url(r'^about/', views.about, name='about'),
    url(r'^gbook/', views.gbook, name='gbook'),
    url(r'^front_index/', views.front_index, name='front_index'),
    url(r'^info/', views.info, name='info'),
    url(r'^infopic/', views.infopic, name='infopic'),
    url(r'^list/', views.list, name='list'),
    url(r'^share/', views.share, name='share'),

    # 访问后台的url
    url(r'^add_article/', views.add_article, name='add_article'),
    url(r'^add_category/', views.add_category, name='add_category'),
    url(r'^add_flink/', views.add_flink, name='add_flink'),
    url(r'^add_notice/', views.add_notice, name='add_notice'),
    url(r'^article/', views.article, name='article'),
    url(r'^category/', views.category, name='category'),
    url(r'^comment/', views.comment, name='comment'),
    url(r'^flink/', views.flink, name='flink'),
    url(r'^back_index/', views.back_index, name='back_index'),
    url(r'^login/', views.login, name='login'),
    url(r'^loginlog/', views.loginlog, name='loginlog'),
    url(r'^manage_user/', views.manage_user, name='manage_user'),
    url(r'^notice/', views.notice, name='notice'),
    url(r'^readset/', views.readset, name='readset'),
    url(r'^setting/', views.setting, name='setting'),
    url(r'^update_article/', views.update_article, name='update_article'),
    url(r'^update_category/', views.update_category, name='update_category'),
    url(r'^update_flink/', views.update_flink, name='update_flink'),

    # 注册
    url(r'^register/', views.register, name='register'),
    # 退出登录
    url(r'^logout/', views.logout, name='logout'),
    # 修改用户信息
    # url(r'^change_message', views.change_message, name='change_message'),
    # 删除文章
    url(r'^delete_article/(\d+)/', views.delete_article, name='delete_article'),

    # only test
    url(r'^test/', views.test, name='test'),
    url(r'^test2/', views.test2, name='test2'),

]
