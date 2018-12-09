#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/23 23:30
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : test.py
# @Software: pycharm

import socket


def get_host_ip():
    """
    查询本机ip地址
    :return: ip
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


print(get_host_ip())

# import socket
#
# # 获取本机计算机名称
# hostname = socket.gethostname()
# # 获取本机ip
# ip = socket.gethostbyname(hostname)
# print(ip)
