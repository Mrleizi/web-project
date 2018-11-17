#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/15 18:59
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : house_views.py
# @Software: pycharm

import os

from flask import Blueprint, render_template, request, jsonify, session

from APP.models import User, House, Area, Facility, HouseImage, Order
from utils import status_code
from utils.fucntions import is_login
from utils.settings import UPLOAD_DIR

house = Blueprint('house', __name__)


@house.route('/auth_myhouse/', methods=['GET'])
@is_login
def auth_myhouse():
    """验证用户是否实名认证"""
    if request.method == 'GET':
        # 获取当前登录用户的编号
        user_id = session['user_id']
        # 根据编号查询当前用户
        user = User.query.get(user_id)
        # 返回用户的真实姓名、身份证号
        if user.id_name:
            # 已经完成实名认证,查询当前用户的房屋信息
            house_list = House.query.filter(House.user_id == user_id).order_by('-id')
            house_list2 = []
            for house in house_list:
                house_list2.append(house.to_dict())
            return jsonify(code='200', hlist=house_list2)
        else:
            # 没有完成实名认证
            return jsonify(status_code.MYHOUSE_USER_IS_NOT_AUTH)


@house.route('/index/', methods=['GET', 'POST'])
def index():
    """爱家首页"""
    return render_template('index.html')


@house.route('/hindex/', methods=['GET'])
def hindex():
    """首页获取信息接口"""
    user_name = ''
    if 'user_id' in session:
        user = User.query.filter_by(id=session['user_id']).first()
        user_name = user.name
        code = status_code.OK
    else:
        code = ''
    # 返回最新的5个房屋信息

    hlist = House.query.order_by(House.id.desc()).all()[:5]
    hlist2 = [house.to_dict() for house in hlist]
    # 查找地区信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]

    return jsonify(code=code, name=user_name, hlist=hlist2, alist=area_dict_list)


@house.route('/area_facility/', methods=['GET'])
@is_login
def area_facility():
    """获取城区、设施"""
    if request.method == 'GET':
        # 获取所有地区
        area_list = Area.query.all()
        area_dict_list = [area.to_dict() for area in area_list]
        # 获取所有设施
        facility_list = Facility.query.all()
        facility_dict_list = [facility.to_dict() for facility in facility_list]
        return jsonify(area=area_dict_list, facility=facility_dict_list)


@house.route('/detail/', methods=['GET', 'POST'])
@is_login
def detail():
    """房间信息"""
    return render_template('detail.html')


@house.route('/detail/<int:id>/', methods=['GET'])
@is_login
def house_detail(id):
    """展示指定房屋信息"""
    if request.method == 'GET':
        # 获取到房屋信息
        house = House.query.get(id)
        # 查询房屋信息
        facility_list = house.facilities
        facility_dict_list = [facility.to_dict() for facility in facility_list]
        # 判断该房屋是否是当前登录的用户发布的，如果是就不显示预定按钮了
        booking = 1
        user_id = session.get('user_id')
        if house.user_id == user_id:
            booking = 0
        return jsonify(house=house.to_full_dict(), booking=booking)


@house.route('/booking/', methods=['GET'])
@is_login
def booking():
    """房间预定"""
    if request.method == 'GET':
        return render_template('booking.html')


@house.route('/myhouse/', methods=['GET', 'POST'])
@is_login
def myhouse():
    """我的房源"""
    return render_template('myhouse.html')


@house.route('/newhouse/', methods=['GET', 'POST'])
@is_login
def newhouse():
    """发布新房源,POST获取房屋信息,及其设施"""
    if request.method == 'GET':
        return render_template('newhouse.html')
    if request.method == 'POST':
        params = request.form.to_dict()
        facility_ids = request.form.getlist('facility')
        # 验证数据的有效性

        # 创建对象并保存
        house = House()
        house.user_id = session['user_id']
        house.area_id = params.get('area_id')
        house.title = params.get('title')
        house.price = params.get('price')
        house.address = params.get('address')
        house.room_count = params.get('room_count')
        house.acreage = params.get('acreage')
        house.unit = params.get('unit')
        house.capacity = params.get('capacity')
        house.beds = params.get('beds')
        house.deposit = params.get('deposit')
        house.min_days = params.get('min_days')
        house.max_days = params.get('max_days')
        # 根据设施的编号查询设施对象
        if facility_ids:
            facility_list = Facility.query.filter(Facility.id.in_(facility_ids)).all()
            house.facilities = facility_list
        house.add_update()
        # 返回结果
        return jsonify(code='200', house_id=house.id)


@house.route('/image/', methods=['POST'])
@is_login
def newhouse_image():
    """房屋图片"""
    if request.method == 'POST':
        # 接收房屋编号
        house_id = request.form.get('house_id')
        # 接收图片信息
        f1 = request.files.get('house_image')
        # 保存到图片
        url = os.path.join(os.path.join(UPLOAD_DIR, 'house'), f1.filename)
        f1.save(url)

        # 保存图片对象
        image = HouseImage()
        image.house_id = house_id
        image.url = os.path.join('/static/media/upload/house', f1.filename)
        image.add_update()
        # 房屋的默认图片
        house = House.query.get(house_id)
        if not house.index_image_url:
            house.index_image_url = os.path.join('/static/media/upload/house', f1.filename)
            house.add_update()
        # 返回图片信息
        # return jsonify(code='200', url=os.path.join('/static/media/upload/house', f1.filename))
        return jsonify(code='200', url=house.index_image_url)


@house.route('/search/', methods=['GET', 'POST'])
def search():
    """搜索房源"""
    return render_template('search.html')


@house.route('/searchall/', methods=['GET'])
def searchall():
    sort_key = request.args.get('sk')  # 对搜索到的房屋排序
    area_id = request.args.get('aid')  # 区域
    begin_date = request.args.get('sd')  # 入住时间
    end_date = request.args.get('ed')  # 离店时间

    houses = House.query.filter_by(area_id=area_id)
    # 排除当前用户自己发布的房源
    user_id = session.get('user_id')
    hlist = houses.filter(House.user_id != user_id)

    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    # 可以的情况:没有交集
    order_list = Order.query.filter(Order.status != 'REJECTED')

    # 情况一：--[---]-- 区间内
    order_list1 = Order.query.filter(Order.begin_date >= begin_date, Order.end_date <= end_date)
    # 情况二：--[---]-- 左外，右外(包含)
    order_list2 = order_list.filter(Order.begin_date < begin_date, Order.end_date > end_date)
    #          ---|
    # 情况三：--[---]-- 左外，右内
    order_list3 = order_list.filter(Order.end_date >= begin_date, Order.end_date <= end_date)
    #             |---
    # 情况四：--[---]-- 左内，右外
    order_list4 = order_list.filter(Order.begin_date >= begin_date, Order.begin_date <= end_date)

    # 获取已经在订单中的房屋编号
    house_ids = [order.house_id for order in order_list1]
    for order in order_list2:
        house_ids.append(order.house_id)
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = hlist.filter(House.id.notin_(house_ids))

    # 排序规则,默认根据最新排列
    sort = House.id.desc()
    if sort_key == 'booking':
        # 按订单数降序排列
        sort = House.order_count.desc()
    elif sort_key == 'price-inc':
        # 按价格升序排列
        sort = House.price.asc()
    elif sort_key == 'price-des':
        # 按价格降序排列
        sort = House.price.desc()
    hlist = hlist.order_by(sort)
    hlist = [house.to_dict() for house in hlist]

    # 获取区域信息
    area_list = Area.query.all()
    area_dict_list = [area.to_dict() for area in area_list]
    return jsonify(code=status_code.OK, houses=hlist, areas=area_dict_list)


# TODO 获取房屋详情可以复用/house/detail/[id]/接口
@house.route('/getbookingbyid/<int:id>/')
def get_booking_by_id(id):
    house = House.query.get(id)
    return jsonify(house=house.to_dict())


if __name__ == '__main__':
    pass
