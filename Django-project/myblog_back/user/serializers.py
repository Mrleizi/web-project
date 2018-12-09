#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/12/3 21:51
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : serializers.py
# @Software: pycharm

from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('name', 'username')


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')


if __name__ == '__main__':
    pass
