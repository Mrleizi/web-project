#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/12 10:10
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : forms.py
# @Software: pycharm

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from users.models import User


class UserRegiterForm(FlaskForm):
    # 定义用户名和密码都是必填项
    username = StringField('账号', validators=[DataRequired()])
    password = StringField('密码', validators=[DataRequired()])
    password2 = StringField('确认密码',
                            validators=[DataRequired(), EqualTo('password', '密码不一致')])
    submit = SubmitField('提交')

    def validate_username(self, field):
        # 验证用户名是否重复
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('用户名已存在')
        if len(field.data) < 3:
            # 对用户名的长度进行判断
            raise ValidationError('注册用户名不能少于3个字符')


if __name__ == '__main__':
    pass
