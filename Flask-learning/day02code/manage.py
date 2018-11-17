#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/9 9:53
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : manage.py
# @Software: pycharm
import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from user.models import db
from user.views import user_blueprint

app = Flask(__name__)
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

# 设置secret_key
app.config['SECRET_KEY'] = '123'

# session配置
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 获取Session对象，并初始化app
se = Session()
se.init_app(app)

# 绑定app和db
db.init_app(app)

manager = Manager(app=app)
if __name__ == '__main__':
    manager.run()
