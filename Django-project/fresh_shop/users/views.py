from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse

from users.forms import UserRegisterForm, UserLoginForm, UserAddressForm
from users.models import User, UserAddress


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')

    if request.method == 'POST':
        # 表单验证， is_valid()
        # 验证通过后。使用自定义的Users.objects.create，在跳转到登录页面
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 保存用户信息
            User.objects.create(username=form.cleaned_data['user_name'],
                                password=make_password(form.cleaned_data['pwd']),
                                email=form.cleaned_data['email'])
            # 注册成功，跳转到登录
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            # 获取当前登录的用户对象
            user = User.objects.filter(username=form.cleaned_data['username']).first()
            # 校验密码是否正确
            if not check_password(form.cleaned_data['pwd'], user.password):
                msg = '密码错误'
                # return HttpResponseRedirect(reverse('users:login'))
                return render(request, 'login.html', {'msg': msg})

            # 添加登录成功的验证
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('home:index'))
        else:
            return render(request, 'login.html', {'form': form})


def is_login(request):
    if request.method == 'GET':
        # 清空session
        user = request.user
        return JsonResponse({'code': 200, 'msg': '请求成功', 'username': user.username})


# 退出登录
def logout(request):
    if request.method == 'GET':
        request.session.flush()
        # session_key = request.session.session_key
        # request.session.delete(session_key)
        return HttpResponseRedirect(reverse('users:login'))


# 个人信息中心
def user_center_info(request):
    if request.method == 'GET':
        return render(request, 'user_center_info.html')


def user_center_site(request):
    if request.method == 'GET':
        user = request.user
        # 获取用户的收货地址信息,默认当前最新的地址
        user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
        return render(request, 'user_center_site.html', {'user_addresses': user_addresses})
    if request.method == 'POST':
        if request.method == 'POST':
            # 使用表单验证，验证收货地址的参数是否填写完整
            form = UserAddressForm(request.POST)
            if form.is_valid():
                user = request.user
                address_info = form.cleaned_data
                # 保存收货地址信息
                UserAddress.objects.create(user=user, **address_info)
                # 保存成功收货地址
                return HttpResponseRedirect(reverse('users:user_center_site'))
            else:
                user = request.user
                # 获取用户的收货地址信息
                user_addresses = UserAddress.objects.filter(user=user).order_by('-id')
                return render(request, 'user_center_site.html', {'form': form, 'user_addresses': user_addresses})


# 设置默认收货地址
def set_default_adress(request):
    if request.method == 'POST':
        user_address_id = request.POST.get('user_address_id')
        user = request.user
        # 获取用户的收货地址信息
        UserAddress.objects.filter(user=user).update(is_default_address=0)
        # 更新默认地址
        UserAddress.objects.filter(pk=user_address_id).update(is_default_address=1)
        return JsonResponse({'code': 200})


# 删除收货地址
def delete_user_address(request):
    if request.method == 'POST':
        user_address_id = request.POST.get('user_address_id')
        # user = request.user
        # 删除地址
        UserAddress.objects.get(pk=user_address_id).delete()
        return JsonResponse({'code': 200})
