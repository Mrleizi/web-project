#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/11 17:12
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : views.py
# @Software: pycharm
import os
import re

from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask import Blueprint, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from werkzeug.utils import secure_filename

from users.forms import UserRegiterForm
from users.models import User, db
from utils.settings import UPLOAD_DIR

user_blueprint = Blueprint('user', __name__)

login_manager = LoginManager()


@user_blueprint.route('/')
def hello_world():
    return 'Hello World!'


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建表成功'


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    form = UserRegiterForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if request.method == 'POST':
        # 判断表单中的数据是否通过验证
        if form.validate_on_submit():
            # 获取验证通过后的数据
            username = form.username.data
            password = form.password.data
            # 实现注册,保存用户信息到User模型中
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            # user.save()
            db.session.add(user)
            db.sessoin.commit()
            return redirect(url_for('user.login'))

        else:
            # 验证失败,form.errors中存在错误信息
            return render_template('register.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # 校验用户名和密码是否填写完整
        if not all([username, password]):
            # 这里也可以进行表单验证,为了简便就省去了,简单验证下就行
            return render_template('login.html')
        user = User.query.filter(User.username == username).first()
        if user:
            # 获取到用户,进行密码判断
            if check_password_hash(user.password, password):
                # 密码正确
                # 实现登录,django中auth.login(request,user)
                login_user(user)
                return redirect(url_for('user.index'))
            else:
                # 密码错误
                error = '密码错误'
                return render_template('login.html', error=error)
        else:
            # 获取不到用户，返回错误信息给页面
            error = '该用户不存在'
            return render_template('login.html', error=error)


@user_blueprint.route('/logout/')
@login_required
def logout():
    logout_user()
    return render_template('login.html')


@user_blueprint.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 获取图片
        icons = request.files.get('icons')
        if icons:
            # 保存save(path)
            # 1.jpg,png...使用正则表达式进行图片格式筛选
            if re.findall(".+(.JPEG|.jpeg|.JPG|.jpg|.GIF|.gif|.BMP|.bmp|.PNG|.png)$", icons.filename):
                file_path = os.path.join(UPLOAD_DIR, icons.filename)
                # file_path = os.path.join(UPLOAD_DIR, secure_filename(icons.filename))

                icons.save(file_path)
                # 保存user对象
                user = current_user
                user.icons = os.path.join('upload', icons.filename)
                user.save()
        return redirect(url_for('user.index'))


# 2.中间件
# @user_blueprint.before_request
# @user_blueprint.after_request
# @user_blueprint.teardown_request


# @user_blueprint.before_request
# def is_login():
#     if request.path == "/user/login/":
#         return None
#
#     if not session.get('user_id'):
#         return redirect(url_for('user.login'))

# @user_blueprint.after_request
# def after_request(response):
#     return '有人访问了我'


if __name__ == '__main__':
    pass
