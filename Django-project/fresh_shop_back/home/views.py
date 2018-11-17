from django.contrib import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from home.forms import UserLoginForm


# 登录
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 1. 表单验证
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # form表单验证成功
            user = auth.authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password'])
            if user:
                # 如果通过username和password获取到user对象，则进行登录
                auth.login(request, user)
                return HttpResponseRedirect(reverse('home:index'))
            else:
                # 用户名或密码错误
                return render(request, 'login.html')

        # 2.auth模块验证
        # 3.auth.login验证
        else:
            # form验证失败，则返回错误信息到页面
            return render(request, 'login.html', {'form': form})


# 首页
def index(request):
    if request.method == 'GET':
        return render(request, 'index.html')


# 退出登录
def logout(request):
    if request.method == 'GET':
        auth.logout(request)
        return HttpResponseRedirect(reverse('home:login'))
