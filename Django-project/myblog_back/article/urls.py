#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/12/3 10:34
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : urls.py
# @Software: pycharm
from django.conf.urls import url
from django.contrib.staticfiles.urls import static

from Myblog import settings
from article import views

urlpatterns = [
    # 文章
    url(r'^article/', views.article, name='article'),
    # 增加文章
    url(r'^add_article/', views.add_article, name='add_article'),
    # 修改文章
    url(r'^update_article/(\d+)/', views.update_article, name='update_article'),
    # 删除文章
    url(r'^delete_article/', views.delete_article, name='delete_article'),
    # 评论
    url(r'^comment/', views.comment, name='comment'),
    # 栏目
    url(r'^category/', views.category, name='category'),
    # 删除栏目
    url(r'^category_delete/', views.category_delete, name='category_delete'),
    # 修改栏目
    url(r'^category_update/(\d+)', views.category_update, name='category_update'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
