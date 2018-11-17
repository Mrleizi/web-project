#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/10 9:35
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : views.py
# @Software: pycharm

from flask import Blueprint
from sqlalchemy import or_, not_, and_

from app.models import db, Students

blue = Blueprint('app', __name__)


@blue.route('/')
def hello():
    return 'hello world'


@blue.route('/create_db/')
def create_db():
    # 用户初次创建模型
    db.create_all()
    return '创建成功'


@blue.route('/drop_db/')
def drop_db():
    # 删除数据库中所有的表
    db.drop_all()
    return '删除成功'


@blue.route('/create_stu/')
def create_stu():
    """增加"""
    # 实现创建，add()
    stu = Students()
    stu.s_name = '雷克顿'
    # db.session.add(stu)
    # db.session.commit()
    stu.save()

    return '创建学生信息成功'


@blue.route('/create_stu_all/')
def create_stu_all():
    # 批量创建,add_all()
    names = ['小李1', '小李2', '小李3', '小李4', '小李5', '小李6', '小李7', '小李8', '小李9', '小李10']
    stu_list = []
    for name in names:
        stu = Students()
        stu.s_name = name
        # stu.save()
        # db.session.add(stu)
        stu_list.append(stu)
    db.session.add_all(stu_list)
    db.session.commit()
    return '批量创建学生成功'


@blue.route('/sel_stu/')
def sel_stu():
    # 查询, filter(),filter_by()
    # 返回类型是querybase
    stu = Students.query.filter(Students.s_name == '小明')
    stu = Students.query.filter_by(s_name='小明')
    # all , first()
    stus = Students.query.all()
    stu = Students.query.filter(Students.s_name == '小明').first()

    # 执行sql
    sql = 'select * from students;'
    stus = db.session.execute(sql)

    # 模糊查询
    # select * from students where s_name like '%小%'
    # select * from students where s_name like '小%'
    # select * from students where s_name like '_明%' 第一个字随意,第二个字为明的同学
    stu = Students.query.filter(Students.s_name.contains('小'))
    stu = Students.query.filter(Students.s_name.like('%小%'))

    # 查询名字以'小'开头的同学
    stu = Students.query.filter(Students.s_name.startswith('小'))
    stu = Students.query.filter(Students.s_name.like('小%'))

    # 查询第一个字随意, 第二个字为'明'的同学
    stu = Students.query.filter(Students.s_name.like('_明%'))

    # 查询id在某个范围之内的学生信息
    # select * from students where id in (1,2,3,4)
    stus = Students.query.filter(Students.id.in_([1, 2, 3, 4]))

    # 查询年龄大于19的学生信息
    stus = Students.query.filter(Students.s_age > 19)
    stus = Students.query.filter(Students.s_age.__gt__(19))

    # 查询id=2的学生信息
    # get()获取主键对应的行数据
    stu = Students.query.get(5)
    # 获取的结果是学生的对象

    # offset+limit
    stus = Students.query.limit(3)
    stus = Students.query.offset(1).limit(3)

    # order_by
    stus = Students.query.order_by('id')
    stus = Students.query.order_by('-id')

    stus = Students.query.order_by('id asc')
    stus = Students.query.order_by('id desc')

    # django中: filter(Q(A) | Q(B))
    # flask中: filter(or_(A,B))
    # 查询姓名中包含'小'，并且年龄等于25
    stus = Students.query.filter(Students.s_name.contains('小'),
                                 Students.s_age == 25)
    stus = Students.query.filter(and_(Students.s_name.contains('小'),
                                      Students.s_age == 25))
    # 查询姓名中包含'小'，或者年龄等于25
    stus = Students.query.filter(or_(Students.s_name.contains('小'),
                                     Students.s_age == 25))

    # 查询姓名中不包含'小'，且年龄等于20
    stus = Students.query.filter(not_(Students.s_name.contains('小')),
                                 Students.s_age == 20)

    return '查询学生'


@blue.route('/delete_stu/<int:id>/')
def delete_stu(id):
    """删除"""
    stu = Students.query.filter(Students.id == id).first()
    db.session.delete(stu)
    db.session.commit()
    return '删除成功'


@blue.route('/update_stu/<int:id>/')
def update_stu(id):
    """修改"""
    stu = Students.query.filter_by(id=id).first()
    stu.s_name = '我爱罗'
    stu.save()
    return '修改成功'


if __name__ == '__main__':
    pass
