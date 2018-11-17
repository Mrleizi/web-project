#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/9 9:54
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : models.py
# @Software: pycharm

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    __tablename__ = 'user'


if __name__ == '__main__':
    pass
