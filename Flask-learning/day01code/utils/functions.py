#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/8 19:27
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : functions.py
# @Software: pycharm
from functools import wraps

from flask import url_for, redirect

# if __name__ == '__main__':
#     pass

from flask import session


def is_login(func):
    @wraps(func)
    def check_status(*args, **kwargs):
        try:
            login_status = session['login_status']
        except:
            return redirect(url_for('app.login'))
        return func(*args, **kwargs)

    return check_status
