#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/9 11:01
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : functions.py
# @Software: pycharm
from functools import wraps

from flask import redirect, url_for, session

# def is_login(func):
#     @wraps(func)
#     def check_status(*args, **kwargs):
#         try:
#             login_status = session['login_status']
#         except:
#             return redirect(url_for('user.login'))
#         return func(*args, **kwargs)
#
#     return check_status
from user.models import User


def is_login(func):
    @wraps(func)
    def check_status(*args, **kwargs):
        try:
            login_username = session['login_username']
            if User.query.filter_by(username=login_username):
                pass
            else:
                return redirect(url_for('user.login'))
        except:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)

    return check_status


if __name__ == '__main__':
    pass
