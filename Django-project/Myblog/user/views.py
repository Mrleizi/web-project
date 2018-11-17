#!/usr/bin/python3
# -*- coding: utf-8 -*-

import platform
import socket
import time

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

# Create your views here.


from user.forms import UserForm, UserLoginForm, AddArticle
from user.models import Admin, Article, Category


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


# 前端页面
def about(request):
    if request.method == 'GET':
        # return render(request, 'index.html')
        # return render(request, 'frontstage/index.html')
        return render(request, 'frontstage/about.html')


def gbook(request):
    if request.method == 'GET':
        return render(request, 'frontstage/gbook.html')


def front_index(request):
    if request.method == 'GET':
        return render(request, 'frontstage/index.html')


def info(request):
    if request.method == 'GET':
        return render(request, 'frontstage/info.html')


def infopic(request):
    if request.method == 'GET':
        return render(request, 'frontstage/infopic.html')


def list(request):
    if request.method == 'GET':
        return render(request, 'frontstage/list.html')


def share(request):
    if request.method == 'GET':
        return render(request, 'frontstage/share.html')


# 后台页面


# 修改用户信息
def change_message(request):
    username = request.POST.get('username')
    old_password = request.POST.get('old_password')
    user = Admin.objects.get(username=username)
    user_password = user.password

    if old_password == user_password:
        new_tel = request.POST.get('usertel')
        password = request.POST('password')
        new_password = request.POST('new_password')
        if password == new_password:
            pass
        else:
            # 两次密码不一致
            pass

    else:
        # 密码错误
        pass
    path = request.path
    analy_url = path.split('/')
    url = HttpResponseRedirect(reverse(analy_url[1] + ':' + analy_url[2]))
    return url


def add_article(request):
    if request.method == 'GET':
        return render(request, 'backstage/add-article.html')
    if request.method == 'POST':
        if len(request.POST) == 6:
            return change_message(request)

        elif len(request.POST) > 6:
            # 增加文章
            art = AddArticle(request.POST, request.FILES)
            if art.is_valid():
                # 验证通过
                # 找到当前的管理员
                username = request.user.username
                category_id = int(art.cleaned_data['category'])
                # Article.objects.create(title=art.cleaned_data['title'],
                #                        content=art.cleaned_data['content'],
                #                        keywords=art.cleaned_data['keywords'],
                #                        tags=art.cleaned_data['tags'],
                #                        titlepic=request.FILES.get('titlepic'),
                #                        describe=art.cleaned_data['describe'],
                #                        is_public=art.cleaned_data['visibility'],
                #                        category=Category.objects.get(id=category_id),
                #                        author=Admin.objects.get(username=username))
                new_article = Article.objects.create(title=art.cleaned_data['title'],
                                                     content=art.cleaned_data['content'],
                                                     keywords=art.cleaned_data['keywords'],
                                                     tags=art.cleaned_data['tags'],
                                                     titlepic=request.FILES.get('titlepic'),
                                                     describe=art.cleaned_data['describe'],
                                                     is_public=art.cleaned_data['visibility'],
                                                     category=Category.objects.get(id=category_id),
                                                     )
                Admin.objects.get(username=username).article_set.add(new_article)
                return HttpResponseRedirect(reverse('user:article'))
            else:
                path = request.path
                analy_url = path.split('/')

                url = HttpResponseRedirect(reverse(analy_url[1] + ':' + analy_url[2]))
                return url


def add_category(request):
    if request.method == 'GET':
        return render(request, 'backstage/add-category.html')
    if request.method == 'POST':
        return change_message(request)


def add_flink(request):
    if request.method == 'GET':
        return render(request, 'backstage/add-flink.html')
    if request.method == 'POST':
        return change_message(request)


def add_notice(request):
    if request.method == 'GET':
        return render(request, 'backstage/add-notice.html')
    if request.method == 'POST':
        return change_message(request)


def article(request):
    if request.method == 'GET':
        # 当前管理员
        current_admin = Admin.objects.get(username=request.user.username)
        arts = current_admin.article_set.all()
        return render(request, 'backstage/article.html', {'arts': arts})
    if request.method == 'POST':
        return change_message(request)


def category(request):
    if request.method == 'GET':
        return render(request, 'backstage/category.html')
    if request.method == 'POST':
        return change_message(request)


def comment(request):
    if request.method == 'GET':
        return render(request, 'backstage/comment.html')
    if request.method == 'POST':
        return change_message(request)


def flink(request):
    if request.method == 'GET':
        return render(request, 'backstage/flink.html')
    if request.method == 'POST':
        return change_message(request)


def back_index(request):
    if request.method == 'GET':
        time1 = time.time()
        admin_record = request.user.loginrecord_set.all()
        login_count = len(admin_record.all())
        admin_count = len(Admin.objects.all())
        login_ip = admin_record.order_by('-id').first().login_ip
        # '''获取操作系统名称及版本号'''
        operate_system = platform.platform()
        try:
            last_time = admin_record.order_by('-id')[1].login_time
            last_ip = admin_record.order_by('-id')[1].login_ip
        except:
            last_time = ''
            last_ip = ''
        return render(request, 'backstage/index.html',
                      {'login_count': login_count, 'last_time': last_time, 'last_ip': last_ip,
                       'admin_count': admin_count, 'login_ip': login_ip, 'operate_system': operate_system,
                       'time1': time1})

    if request.method == 'POST':
        if len(request.POST) == 6:
            return change_message(request)
        else:
            path = request.path
            analy_url = path.split('/')

            url = HttpResponseRedirect(reverse(analy_url[1] + ':' + analy_url[2]))
            return url


def login(request):
    if request.method == 'GET':
        return render(request, 'backstage/login.html')
    if request.method == 'POST':
        # 使用cookie+session形式实现登陆
        username = request.POST.get('username')
        password = request.POST.get('password')

        # all()校验参数，如果列表中元素为空，则返回False
        if not all([username, password]):
            msg = 'Please fill in the complete parameters !'
            return render(request, 'backstage/login.html', {'msg': msg})
        # 校验是否能通过username和password找到user对象
        user = Admin.objects.filter(username=username).first()
        if user:
            if not check_password(password, user.password):
                msg = 'username or password error !'
                return render(request, 'backstage/login.html', {'msg': msg})
            else:
                # 向cookie中设值，向user_ticket表中设值(这里用的是django中的django_session表) 一句话解决
                request.session['user_id'] = user.id
                # 设置session过期时间
                # request.session.set_expiry(600)
                # 获取当前登录的ip
                ip = get_host_ip()
                # 本次登录的ip
                user.loginrecord_set.create(login_ip=ip)
                return HttpResponseRedirect(reverse('user:back_index'))
        else:
            msg = 'username or password error !'
            return render(request, 'backstage/login.html', {'msg': msg})


def loginlog(request):
    if request.method == 'GET':
        return render(request, 'backstage/loginlog.html')
    if request.method == 'POST':
        return change_message(request)


def manage_user(request):
    if request.method == 'GET':
        return render(request, 'backstage/manage-user.html')
    if request.method == 'POST':
        return change_message(request)


def notice(request):
    if request.method == 'GET':
        return render(request, 'backstage/notice.html')
    if request.method == 'POST':
        return change_message(request)


def readset(request):
    if request.method == 'GET':
        return render(request, 'backstage/readset.html')
    if request.method == 'POST':
        return change_message(request)


def setting(request):
    if request.method == 'GET':
        return render(request, 'backstage/setting.html')
    if request.method == 'POST':
        return change_message(request)


def update_article(request):
    if request.method == 'GET':
        return render(request, 'backstage/update-article.html')


def update_category(request):
    if request.method == 'GET':
        return render(request, 'backstage/update-category.html')
    if request.method == 'POST':
        return change_message(request)


def update_flink(request):
    if request.method == 'GET':
        return render(request, 'backstage/update-flink.html')


def test(request):
    if request.method == 'GET':
        return render(request, 'frontstage/list.html')


# 这里开始测试了
def test(request):
    if request.method == 'GET':
        # return render(request, 'frontstage/about01.html')
        # return render(request, 'frontstage/base_main.html')
        # return render(request, 'frontstage/about.html')
        # return render(request, 'frontstage/gbook.html')
        # return render(request, 'frontstage/infopic.html')
        # return render(request, 'frontstage/index.html')
        # return render(request, 'frontstage/info.html')
        # return render(request, 'frontstage/list.html')
        return render(request, 'frontstage/share.html')


def test2(request):
    if request.method == 'GET':
        return render(request, 'backstage/test2.html')
        # return render(request, 'backstage/add-article222.html')
        # return render(request, 'backstage/add-article222.html')
        # return render(request, 'backstage/add-article.html')
        # return render(request, 'backstage/add-category.html')
        # return render(request, 'backstage/add-flink.html')
        # return render(request, 'backstage/add-notice.html')
        # return render(request, 'backstage/article.html')
        # return render(request, 'backstage/category.html')
        # return render(request, 'backstage/comment.html')
        # return render(request, 'backstage/flink.html')
        # return render(request, 'backstage/index.html')
        # return render(request, 'backstage/login.html')
        # return render(request, 'backstage/loginlog.html')
        # return render(request, 'backstage/manage-user.html')
        # return render(request, 'backstage/notice.html')
        # return render(request, 'backstage/readset.html')
        # return render(request, 'backstage/setting.html')
        # return render(request, 'backstage/update-article.html')
        # return render(request, 'backstage/update-category.html')
        # return render(request, 'backstage/update-flink.html')


# 注册
def register(request):
    if request.method == 'GET':
        # 如果请求为get，返回注册页面
        return render(request, 'backstage/register.html')
    if request.method == 'POST':
        # 校验参数
        form = UserForm(request.POST)
        # 判断is_valid（）是否为True
        if form.is_valid():
            # 注册,使用make_password进行密码加密，否则[数据库中]为明文
            password = make_password(form.cleaned_data['password'])
            Admin.objects.create(name=form.cleaned_data['name'],
                                 tel=form.cleaned_data['tel'],
                                 username=form.cleaned_data['username'],
                                 password=password, )
            # 跳转到登录页面,使用namespace:name
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request, 'backstage/register.html', {'form': form})


# 退出登录
def logout(request):
    if request.method == 'GET':
        request.session.flush()
        return HttpResponseRedirect(reverse('user:login'))


# 删除文章
def delete_article(request, id):
    if request.method == 'GET':
        # 找到当前管理员
        current_admin = Admin.objects.get(username=request.user.username)
        art = current_admin.article_set.get(pk=id)
        current_admin.article_set.remove(art)
        return HttpResponseRedirect(reverse('user:article'))
