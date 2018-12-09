# -*- coding: utf-8 -*-

# from django.contrib.auth.models import AbstractUser

from django.db import models


# Create your models here.

class User(models.Model):
    """管理员表"""
    truename = models.CharField(max_length=100, null=False, verbose_name='姓名')
    username = models.CharField(max_length=100, unique=True, null=False, verbose_name='用户名')
    password = models.CharField(max_length=225, null=False, verbose_name='密码')
    usertel = models.CharField(max_length=12, null=False, verbose_name='电话')

    class Meta:
        db_table = "user"


class Notice(models.Model):
    """公告表"""
    title = models.CharField(max_length=200, null=False, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    keywords = models.CharField(max_length=200, verbose_name='关键字')
    describe = models.TextField(null=True, verbose_name='描述')
    time = models.DateTimeField(auto_now_add=True, verbose_name='公告发布日期')
    visibility = models.BooleanField(default=True, verbose_name='是否公开')

    announcer = models.ForeignKey(User, null=True, verbose_name='公告发布者')

    class Meta:
        db_table = 'notice'


class Flink(models.Model):
    """友情链接表"""
    name = models.CharField(max_length=200, null=False, verbose_name='名称')
    url = models.CharField(max_length=500, null=False, verbose_name='图像地址')
    imgurl = models.CharField(max_length=500, null=False, verbose_name='图像地址')
    describe = models.TextField(null=True, verbose_name='描述')
    target = models.IntegerField(choices=((0, '_blank'), (1, '_self'), (2, '_top')), verbose_name='跳转页面的方式给')

    rel = models.IntegerField(choices=((0, 'nofollow'), (1, 'none')))
    time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    editor = models.ForeignKey(User, null=False, verbose_name='友情链接编辑者')

    class Meta:
        db_table = 'flink'


class LoginLog(models.Model):
    """登录记录表"""
    # 所有管理员和用户都有
    login_ip = models.CharField(max_length=50, verbose_name='登录者ip')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')

    loginer = models.ForeignKey(User, null=False)

    class Meta:
        db_table = 'loginlog'
