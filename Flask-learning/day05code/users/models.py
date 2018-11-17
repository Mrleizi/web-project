#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/12 10:10
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : models.py
# @Software: pycharm

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    password = db.Column(db.String(130), nullable=False)
    icons = db.Column(db.String(255), nullable=True)

    __tablename__ = 'user'

    def save(self):
        db.session.add(self)
        db.session.commit()


if __name__ == '__main__':
    pass
