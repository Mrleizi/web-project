#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/15 10:37
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : user_views.py
# @Software: pycharm
import os
import re

from flask import Blueprint, render_template, request, jsonify, session

from APP.models import db, User
from utils import status_code
from utils.fucntions import is_login
from utils.settings import UPLOAD_DIR

user = Blueprint('user', __name__)


@user.route('/')
def hello_world():
    return 'Hello World!'


@user.route('/create_db/')
def create_db():
    # 用户初次创建模型
    db.create_all()
    # return jsonify(status_code.SUCCESS)
    return '创建表成功'


@user.route('/register/', methods=['GET', 'POST'])
def register():
    """注册"""
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        # imagecode = request.form.get('imagecode')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        # 验证参数是否填完
        if not all([mobile, password, password2]):
            return jsonify(status_code.PARAMS_ERROR)
        # 验证手机号码格式是否正确
        if not re.fullmatch(r'^1[34578]\d{9}$', mobile):
            return jsonify(status_code.USER_LOGIN_PHONE_ERROR)
        # 验证手机号是否已经注册过
        if User.query.filter_by(phone=mobile).first():
            return jsonify(status_code.USER_REGISTER_USER_PHONE_EXSITS)

        # 若全部验证成功
        user = User()
        user.name = mobile
        user.phone = mobile
        user.password = password
        try:
            user.add_update()
            return jsonify(status_code.SUCCESS)
        except:
            return jsonify(status_code.USER_REGISTER_USER_ERROR)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    """登录"""
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('mobile')
        password = request.form.get('password')
        user = User.query.filter_by(phone=username).first()
        if not user:
            return jsonify(status_code.USER_LOGIN_USER_NOT_EXSITS)
        if not user.check_pwd(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_ERROR)
        session['user_id'] = user.id
        return jsonify(status_code.SUCCESS)


@user.route('/logout/', methods=['DELETE'])
@is_login
def logout():
    """退出登录"""
    if request.method == 'DELETE':
        session.pop('user_id')
        return jsonify(status_code.SUCCESS)


@user.route('/my/', methods=['GET', 'POST'])
@is_login
def my():
    """个人信息界面"""
    if request.method == 'GET':
        user = User.query.get(session['user_id'])

        return render_template('my.html', user=user)
    if request.method == 'POST':
        pass


@user.route('/profile/', methods=['GET', 'PUT'])
@is_login
def profile():
    """修改个人信息界面"""
    if request.method == 'GET':
        return render_template('profile.html')
    if request.method == 'PUT':
        dict = request.form
        dict_file = request.files
        if 'avatar' in dict_file:
            try:
                # 获取头像文件
                f1 = request.files['avatar']
                # mime-type:国际规范，表示文件的类型，如text/html,text/xml,image/png,image/jpeg..
                if not re.match('image/.*', f1.mimetype):
                    return jsonify(status_code.USER_PROFILE_IMAGE_UPDATE_ERROR)
            except:
                return jsonify(code=status_code.PARAMS_ERROR)
            # 保存到upload中
            url = os.path.join(os.path.join(UPLOAD_DIR, 'avatar'), f1.filename)
            f1.save(url)

            # 如果未出错
            # 保存用户的头像信息
            try:
                user = User.query.get(session['user_id'])
                user.avatar = os.path.join('/static/media/upload/avatar', f1.filename)
                user.add_update()
            except:
                return jsonify(status_code.DATABASE_ERROR)
            # 则返回图片信息
            # return jsonify(code='200', url=os.path.join('/static/media/upload', f1.filename))
            return jsonify(code='200', url=user.avatar)

        elif 'name' in dict:
            # 修改用户名
            name = dict.get('name')
            # 判断用户名是否存在
            if User.query.filter_by(name=name).count():
                return jsonify(status_code.USER_REGISTER_USER_IS_EXSITS)
            else:
                user = User.query.get(session['user_id'])
                user.name = name
                user.add_update()
                return jsonify(status_code.SUCCESS)
        else:
            return jsonify(status_code.PARAMS_ERROR)


@user.route('/auth/', methods=['GET', 'POST', 'PUT'])
@is_login
def auth():
    """实名认证"""
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        return render_template('auth.html', user=user)

    if request.method == 'PUT':
        real_name = request.form.get('real_name')
        id_card = request.form.get('id_card')
        # 验证是否填写参数
        if not all([real_name, id_card]):
            return jsonify(status_code.PARAMS_ERROR)
        # 身份证号是否合法
        if not re.match(r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)', id_card):
            return jsonify(status_code.USER_REGISTER_AUTH_ERROR)
        try:
            user = User.query.get(session['user_id'])
        except:
            return jsonify(status_code.DATABASE_ERROR)
        try:
            user.id_name = real_name
            user.id_card = id_card
            user.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)
        # 修改成功返回数据
        return jsonify(status_code.SUCCESS)


@user.route('/auths/', methods=['GET'])
@is_login
def user_auth():
    """验证用户是否实名认证"""
    if request.method == 'GET':
        # 获取当前登录用户的编号
        user_id = session['user_id']
        # 根据编号查询当前用户
        user = User.query.get(user_id)
        # 返回用户的真实姓名、身份证号
        if user.id_name:
            return jsonify(user.to_auth_dict())


if __name__ == '__main__':
    pass
