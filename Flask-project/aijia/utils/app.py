#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/18 15:07
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : app.py
# @Software: pycharm
from flask import Flask

from APP.user_views import user
from APP.house_views import house
from APP.order_views import order

from utils.fucntions import init_ext
from utils.settings import STATIC_DIR, TEMPLATES_DIR


def create_app(Config):
    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)

    app.register_blueprint(blueprint=user, url_prefix='/user')
    app.register_blueprint(blueprint=house, url_prefix='/house')
    app.register_blueprint(blueprint=order, url_prefix='/order')

    # 配置
    app.config.from_object(Config)
    # 初始化各种第三方库
    init_ext(app)

    return app


if __name__ == '__main__':
    pass
