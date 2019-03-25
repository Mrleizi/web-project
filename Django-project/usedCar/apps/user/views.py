from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from apps.car.models import Carinfo
from apps.user.models import User
from apps.user.forms import UserRegisterForm, UserIdentifyForm
from utils.functions import is_login


def login_status(request):
    if request.method == 'GET':
        username = request.session.get('username')
        return JsonResponse({'code': 200, 'username': username})


def register(request):
    """用户注册"""
    if request.method == 'GET':
        cellphone = request.GET.get('cellphone')
        return render(request, 'register.html', {'cellphone': cellphone})
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.cleaned_data['userpwd'] = make_password(form.cleaned_data.pop('reuserpwd'))
            User.objects.create(**form.cleaned_data)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    """用户登录"""
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        userpwd = request.POST.get('userpwd')
        user = User.objects.filter(username=username).first()
        if user:
            if check_password(userpwd, user.userpwd):
                request.session['username'] = user.username
                request.user = user
                return HttpResponseRedirect(reverse('index'))
            else:
                msg = '用户名或密码错误'
                return render(request, 'login.html', {'msg': msg})
        else:
            msg2 = '用户名或密码错误'
            return render(request, 'login.html', {'msg2': msg2})


@is_login
def user_info(request):
    """用户个人信息"""
    if request.method == 'GET':
        cars = Carinfo.objects.filter(user=request.user)
        return render(request, 'user-info.html', {'cars': cars})
    if request.method == 'POST':
        user = request.user
        user.realname = request.POST.get('name')
        user.sex = request.POST.get('sex')
        user.cellphone = request.POST.get('phone')
        user.uidentity = request.POST.get('uidentity')
        user.save()
        return render(request, 'user-info.html')


@is_login
def buyregister(request):
    """买家中心,信息完善"""
    if request.method == 'GET':
        return render(request, 'buyregister.html')
    if request.method == 'POST':
        user = request.user

        form = UserIdentifyForm(request.POST)
        if form.is_valid():
            user.realname = form.cleaned_data.get('realname')
            user.uidentity = form.cleaned_data.get('identity')
            user.address = form.cleaned_data.get('address')
            user.cellphone = form.cleaned_data.get('phone')
            user.sex = request.POST.get('gender')
            user.save()
            return HttpResponseRedirect(reverse('car:carlist'))
        else:
            return render(request, 'buyregister.html', {'form': form})


@is_login
def user_logout(request):
    """退出登录"""
    request.session.flush()
    return HttpResponseRedirect(reverse('index'))


def service(request):
    """服务页面"""
    return render(request, 'service.html')


def protection(request):
    """服务保障"""
    return render(request, 'protection.html')
