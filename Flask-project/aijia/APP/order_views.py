#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/15 19:03
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : order_views.py
# @Software: pycharm

from datetime import datetime

from flask import Blueprint, render_template, request, jsonify, session

from APP.models import House, Order
from utils import status_code
from utils.fucntions import is_login

order = Blueprint('order', __name__)


@order.route('/placeorder/', methods=['POST'])
@is_login
def book():
    """作为租客 下单"""
    if request.method == 'POST':
        dict = request.form
        house_id = int(dict.get('house_id'))
        start_date = datetime.strptime(dict.get('start_date'), '%Y-%m-%d')
        end_date = datetime.strptime(dict.get('end_date'), '%Y-%m-%d')
        # 验证有效性
        if not all([house_id, start_date, end_date]):
            return jsonify(status_code.PARAMS_ERROR)
        if start_date > end_date:
            return jsonify(status_code.ORDER_START_END_TIME_ERROR)
        # 查询房屋对象
        try:
            house = House.query.get(house_id)
        except:
            return jsonify(status_code.DATABASE_ERROR)
        # 创建订单对象
        order = Order()
        order.user_id = session['user_id']
        order.house_id = house_id
        order.begin_date = start_date
        order.end_date = end_date
        order.days = (end_date - start_date).days + 1
        order.house_price = house.price
        order.amount = order.days * order.house_price

        try:
            order.add_update()
        except:
            return jsonify(status_code.DATABASE_ERROR)

        # 返回信息
        return jsonify(code=status_code.OK)


@order.route('/orders/', methods=['GET', 'POST'])
@is_login
def orders():
    """作为租客，我提交的订单"""
    if request.method == 'GET':
        return render_template('orders.html')


@order.route('/renter/', methods=['GET'])
@is_login
def my_orders():
    """作为租客 查看我的订单"""
    if request.method == 'GET':
        user_id = session['user_id']
        orders = Order.query.filter(Order.user_id == user_id).order_by(Order.id.desc())
        orders_list = [order.to_dict() for order in orders]
        return jsonify(olist=orders_list)


@order.route('/lorders/', methods=['GET', 'POST'])
@is_login
def lorders():
    """作为房东,查看客户提交的订单"""
    if request.method == 'GET':
        return render_template('lorders.html')


@order.route('/lorders_list/', methods=['GET'])
@is_login
def landlord():
    """作为房东 查看客户订单接口"""
    if request.method == 'GET':
        user_id = session['user_id']
        # 查询当前用户的所有房屋
        hlist = House.query.filter(House.user_id == user_id)
        hid_list = [house.id for house in hlist]
        # 根据房屋编号查找订单
        order_list = Order.query.filter(Order.house_id.in_(hid_list)).order_by(Order.id.desc())
        # 构造结果
        olist = [order.to_dict() for order in order_list]
        return jsonify(olist=olist)


@order.route('/order/<int:id>/', methods=['PUT'])
@is_login
def status(id):
    """修改订单状态"""
    # 接收参数：状态
    status = request.form.get('status')
    # 查找订单对象
    order = Order.query.get(id)
    # 修改订单状态
    order.status = status
    # 如果是拒单，需要添加原因
    if status == 'REJECTED':
        if request.form.get('comment'):
            order.comment = request.form.get('comment')
        else:
            return jsonify(status_code.PARAMS_ERROR)
    # 保存
    try:
        order.add_update()
    except:
        return jsonify(status_code.DATABASE_ERROR)

    return jsonify(code=status_code.OK)


@order.route('/booking/', methods=['GET', 'POST'])
def booking():
    """预定"""
    if request.method == 'GET':
        return render_template('booking.html')


if __name__ == '__main__':
    pass
