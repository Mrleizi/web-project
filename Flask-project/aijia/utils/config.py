#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/18 15:20
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : config.py
# @Software: pycharm

from utils.fucntions import get_mysql_url, get_redisdb_url


class Config():
    # 配置数据库
    SQLALCHEMY_DATABASE_URI = get_mysql_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # session的配置
    SECRET_KEY = 'secret_key'
    SESSION_TYPE = 'redis'
    SESSIOIN_REDIS = get_redisdb_url()


if __name__ == '__main__':
    pass
