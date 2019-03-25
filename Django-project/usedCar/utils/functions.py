# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.urls import reverse

from apps.user.models import User

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


def is_login(func):
    def check(request, *args, **kwargs):
        username = request.session.get('username')
        if username:
            user = User.objects.filter(username=username).first()
            if user:
                request.user = user
                return func(request, *args, **kwargs)
            else:
                return HttpResponseRedirect(reverse('user:login'))

        else:
            return HttpResponseRedirect(reverse('user:login'))

    return check
