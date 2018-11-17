#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/9/28 17:17
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : functions.py
# @Software: pycharm

import random
from datetime import datetime


def get_order_sn():
    """
    生成随机的订单号
    """
    sn = ''
    s = '1234567890qwertyuiopasdfghjklzxcvbnm'
    for i in range(10):
        sn += random.choice(s)
    sn += datetime.now().strftime('%Y%m%d%H%M%S')
    return sn
