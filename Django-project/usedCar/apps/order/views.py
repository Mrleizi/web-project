from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from utils.functions import is_login, get_order_sn
from apps.car.models import Carinfo
from apps.order.models import Orders


@is_login
def create_order(request, id):
    """生成订单"""
    if request.method == 'GET':
        car = Carinfo.objects.filter(id=id).first()
        sale_user = car.user
        buy_user = request.user
        orderNo = get_order_sn()

        data_dict = {
            'sale_user': sale_user, 'buy_user': buy_user, 'car': car, 'orderNo': orderNo
        }
        order = Orders.objects.create(**data_dict)
        return HttpResponseRedirect('/order/order/{}'.format(order.id))


@is_login
def order(request, id):
    """显示订单"""
    order = Orders.objects.filter(id=id).first()
    return render(request, 'order.html', {'order': order})


@is_login
def cancel_order(request, id):
    if request.method == 'GET':
        order = Orders.objects.filter(id=id).first()
        order.orderStatus = 3
        order.save()
        return render(request, 'order.html', {'order': order})


@is_login
def ensure_order(request, id):
    if request.method == 'GET':
        order = Orders.objects.filter(id=id).first()
        order.orderStatus = 2
        order.save()
        return render(request, 'order.html', {'order': order})
