#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/9 9:54
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : views.py
# @Software: pycharm

import hashlib

from flask import Blueprint, render_template, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from user.models import db, User
from utils.functions import is_login

# 第一步，获取蓝图,指定蓝图别名为app

user_blueprint = Blueprint('user', __name__)


# @user_blueprint.route('/login/', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return render_template('login.html')
#
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#         # 校验用户名和密码，不能为空
#         if not all([username, password]):
#             return render_template('login.html')
#         if username == 'coco' and password == '123456':
#             session['login_status'] = 33
#             return redirect(url_for('user.index'))
#         else:
#             return render_template('login.html')

@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # 'jg4myaxtt8xbvy2b9pdzhjsfugldmdjt'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        # 校验用户名和密码，不能为空
        if not all([username, password]):
            return render_template('login.html')
        if username:
            if check_password_hash(user.password, password):
                # if check_password_hash(password, user.password):
                session['login_username'] = username
                return redirect(url_for('user.index'))
            else:
                return render_template('login.html')
        else:
            return render_template('login.html')


@user_blueprint.route('/index/', methods=['GET', 'POST'])
@is_login
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        session.clear()
        return redirect(url_for('user.login'))


@user_blueprint.route('/scores/', methods=['GET'])
def socres():
    stu_scores = [89, 39, 100, 34, 60, 80, 90]
    content_h2 = '<h2 style="color:blue">hello python</h2>'
    return render_template('scores.html', stu_scores=stu_scores, content_h2=content_h2)


@user_blueprint.route('/create_db/')
def create_db():
    db.create_all()
    return '创建表成功'


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            return render_template('register.html', requered='用户名和密码必填')
        if User.query.filter_by(username=username).first():
            return render_template('register.html', msg='用户名已存在')
        # 保存注册信息
        user = User()
        user.username = username
        # 密码加密
        user.password = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))


@user_blueprint.route('/select/')
def select():
    # 查询所有
    # students = User.query.all() # 无.first()用法  有下标用法[0] ,因为是一个列表

    # 过滤
    # 方法1
    # students = User.query.filter(User.id == 1) # 有.first()用法 也有下标用法[0]

    # 方法2
    students = User.query.filter_by(id=1)  # 有.first()用法 也有下标用法[0]

    # 方法3
    # sql = 'select * from user where id=1'
    # students = db.session.execute(sql)  # 有.first()用法 无下标用法[0]
    return render_template('students.html', students=students)


if __name__ == '__main__':
    pass
