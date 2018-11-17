#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/8 9:26
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : manage.py
# @Software: pycharm

from flask import Flask
from flask_script import Manager

from app.views import blue

app = Flask(__name__)

# 第二步，绑定蓝图blue和app的关系
app.register_blueprint(blueprint=blue, url_prefix='/app')

# 设置secret_key
app.config['SECRET_KEY'] = '123'

# 将flask对象交给Manager管理，并且启动方式修改为manager.run()
manager = Manager(app=app)
if __name__ == '__main__':
    # app.run()
    # 修改启动的ip和端口,debug模式
    # app.run(host='0.0.0.0', port=8092, debug=True)

    # python xxx.py runserver -h 0.0.0.0 -p 8080 -d
    manager.run()
