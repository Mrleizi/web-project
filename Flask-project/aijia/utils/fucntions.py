#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/15 16:53
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : fucntions.py
# @Software: pycharm
import functools

import redis
from flask import redirect, session, url_for
from flask_session import Session

from APP.models import User, db
from utils.settings import REDIS_DATABASE, MYSQL_DATABASES


def init_ext(app):
    """绑定app和db"""
    db.init_app(app)
    # 绑定session和app
    sess = Session()
    sess.init_app(app)


def get_mysql_url():
    # 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'
    DRIVER = MYSQL_DATABASES['DRIVER']
    DH = MYSQL_DATABASES['DH']
    ROOT = MYSQL_DATABASES['ROOT']
    PASSWORD = MYSQL_DATABASES['PASSWORD']
    HOST = MYSQL_DATABASES['HOST']
    POST = MYSQL_DATABASES['POST']
    NAME = MYSQL_DATABASES['NAME']

    return '{}+{}://{}:{}@{}:{}/{}'.format(DRIVER, DH, ROOT, PASSWORD, HOST, POST, NAME)
    # return '%s+%s://%s:%s@%s:%s/%s' % (DRIVER, DH, ROOT, PASSWORD, HOST, POST, NAME)
    # return 'mysql+pymysql://root:123456@127.0.0.1:3306/ihome'


def get_redisdb_url():
    host = REDIS_DATABASE['HOST']
    port = REDIS_DATABASE['PORT']
    return redis.Redis(host=host, port=port)


def is_login(func):
    @functools.wraps(func)
    def check_status(*args, **kwargs):
        try:
            user_id = session['user_id']
            if User.query.filter_by(id=user_id):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('user.login'))
        except:
            return redirect(url_for('user.login'))

    return check_status


if __name__ == '__main__':
    pass
