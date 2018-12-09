#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render

from user.forms import UserForm, UserLoginForm, UserUpdateForm, NoticeForm, FlinkForm
from user.models import User, Notice, Flink, LoginLog


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


def register(request):
    """注册"""
    if request.method == 'GET':
        # 如果请求为get，返回注册页面
        return render(request, 'register.html')

    if request.method == 'POST':
        # 校验参数
        form = UserForm(request.POST)
        # 判断is_valid（）是否为True
        if form.is_valid():
            # 注册,使用make_password进行密码加密，否则[数据库中]为明文
            password = make_password(form.cleaned_data['password'])
            data = form.cleaned_data
            data['password'] = password
            data.pop('password2')
            User.objects.create(**data)

            # 跳转到登录页面,使用namespace:name
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    """登录"""
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        # 使用cookie+session形式实现登陆
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=request.POST.get('username')).first()
            request.session['username'] = user.username
            ip = get_host_ip()
            LoginLog.objects.create(login_ip=ip, loginer=user)
            return HttpResponseRedirect(reverse('user:index'))
        else:
            return render(request, 'login.html', {'form': form})


def index(request):
    if request.method == 'GET':
        # 管理员人数
        admin_count = User.objects.all().count()
        # 登陆者
        user = request.user
        return render(request, 'index.html', {'admin_count': admin_count, 'user': user})


def logout(request):
    """退出登录"""
    if request.method == 'GET':
        request.session.flush()
        # session_key = request.session.session_key
        # request.session.delete(session_key)
        return HttpResponseRedirect(reverse('user:login'))


def personal_details(request):
    """登陆者详细信息"""
    if request.method == 'POST':
        user = request.user
        if check_password(request.POST.get('old_password'), user.password):
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                data['password'] = make_password(data.pop('password2'))
                User.objects.filter(username=user.username).update(**data)
                request.user = User.objects.filter(username=form.cleaned_data.get('username')).first()
                request.session['username'] = request.user.username
                return JsonResponse({'code': 200, 'username': request.user.username})
        else:
            msg = '密码不正确'
            return JsonResponse({'code': 400, 'msg': msg})


def notice(request):
    """公告"""
    if request.method == 'GET':
        notices = Notice.objects.all()
        return render(request, 'notice.html', {'notices': notices})
    if request.method == 'POST':
        """删除选中的公告"""
        notice_ids = request.POST.getlist('checkbox[]')
        Notice.objects.filter(id__in=notice_ids).delete()
        return HttpResponseRedirect(reverse('user:notice'))


def add_notice(request):
    """增加公告"""
    if request.method == 'GET':
        return render(request, 'add-notice.html')
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['announcer'] = request.user
            Notice.objects.create(**data)
            return HttpResponseRedirect(reverse('user:notice'))
        else:
            return render(request, 'add-notice.html', {'form': form})


def delete_notice(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        Notice.objects.filter(id=id).delete()
        return JsonResponse({'code': 200})


def flink(request):
    if request.method == 'GET':
        flinks = Flink.objects.all()
        return render(request, 'flink.html', {'flinks': flinks})
    if request.method == 'POST':
        """删除选中的友情链接"""
        flink_ids = request.POST.getlist('checkbox[]')
        Flink.objects.filter(id__in=flink_ids).delete()
        return HttpResponseRedirect(reverse('user:flink'))


def add_flink(request):
    """添加友情链接"""
    if request.method == 'GET':
        return render(request, 'add-flink.html')
    if request.method == 'POST':
        form = FlinkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['editor'] = request.user
            Flink.objects.create(**data)
            return HttpResponseRedirect(reverse('user:flink'))
        else:
            return render(request, 'add-flink.html', {'form': form})


def update_flink(request, id):
    """修改友情链接"""
    if request.method == 'GET':
        flink = Flink.objects.filter(pk=id).first()
        return render(request, 'update-flink.html', {'flink': flink})
    if request.method == 'POST':
        form = FlinkForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Flink.objects.filter(pk=id).update(**data)
            return HttpResponseRedirect(reverse('user:flink'))
        else:
            return render(request, 'update-flink.html', {'form': form})


def delete_flink(request):
    """删除友情链接"""
    if request.method == 'POST':
        flink_id = request.POST.get('id')
        Flink.objects.filter(pk=flink_id).delete()
        return JsonResponse({'code': 200})


def loginlog(request):
    """登录记录"""
    if request.method == 'GET':
        loginlogs = LoginLog.objects.all()
        return render(request, 'loginlog.html', {'loginlogs': loginlogs})


def delete_loginlog(request):
    """清除登录记录"""
    if request.method == 'POST':
        id = request.POST.get('id')
        LoginLog.objects.filter(pk=id).delete()
        return HttpResponseRedirect(reverse('user:loginlog'))


def delete_uloginlog(request):
    """清除本人登录记录"""
    if request.method == 'GET':
        LoginLog.objects.filter(loginer=request.user).delete()
        return HttpResponseRedirect(reverse('user:loginlog'))


def delete_aloginlog(request):
    """清除所有登录记录"""
    if request.method == 'GET':
        LoginLog.objects.all().delete()
        return HttpResponseRedirect(reverse('user:loginlog'))


def manage_user(request):
    """管理用户"""
    if request.method == 'GET':
        users = User.objects.all()
        return render(request, 'manage-user.html', {'users': users})


def delete_user(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = User.objects.filter(pk=id).first()
        # 删除所有登录记录
        user.loginlog_set.all().delete()
        # 删除所有文章
        user.article_set.all().delete()
        # 删除用户
        user.delete()

        return JsonResponse({'code': 200})


def setting(request):
    """基本设置"""
    if request.method == 'GET':
        return render(request, 'setting.html')


def readset(request):
    """阅读设置"""
    if request.method == 'GET':
        return render(request, 'readset.html')
