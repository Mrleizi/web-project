#!/usr/bin/python3
# -*- coding: utf-8 -*-

# @Time    : 2018/10/10 9:35
# @Author  : helei
# @Email   : 1982540042@qq.com
# @File    : views.py
# @Software: pycharm
from random import choice
from random import randint

from flask import Blueprint, request, render_template
from sqlalchemy import or_, not_, and_

from app.models import db, Students, Grade, Course

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
    names = ['金克斯', '吉格斯', '艾莉丝', '伊丽丝', '贾克斯', '拉克丝', '戴安娜',
             '维鲁斯', '拉莫斯', '杰斯', '内瑟斯', '科加斯', '泽拉斯', '斯维因']
    grade_list = Grade.query.all()
    g_ids = []
    for grade in grade_list:
        g_ids.append(grade.id)
    stu_list = []
    for name in names:
        stu = Students()
        stu.s_name = name
        stu.age = randint(20, 30)
        stu.s_g = choice(g_ids)
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


# 实现分页
@blue.route('/paginate/')
def stu_page():
    # 切片 offest sql语句 paginate()方法
    # 切片
    page = int(request.args.get('page', 1))
    page_list = Students.query.all()[3 * page - 1:3 * page]

    # offset
    stus = Students.query.offset((page - 1) * 3).limit(3)

    # sql语句
    sql = 'select * from students limit %s,%s' % ((page - 1) * 3, page * 3)
    stus = db.session.execute(sql)

    # paginate()方法
    paginate = Students.query.paginate(page, 3)
    stus = paginate.items
    return render_template('stus.html', stus=stus, paginate=paginate)


@blue.route('/create_grade_all/')
def create_grade_all():
    grade_names = ['python', 'java', 'html5', 'php', 'matlab', 'C++']
    g_names = []
    for g_name in grade_names:
        grade = Grade()
        grade.g_name = g_name
        g_names.append(grade)
    db.session.add_all(g_names)
    db.session.commit()
    return '创建所有年级成功'


# 添加学生和班级的关联关系
@blue.route('/rel_stu_grade/')
def rel_stu_grade():
    stud_ids = [15, 16, 17]
    for id in stud_ids:
        stu = Students.query.get(id)
        # 在django中 stu.s_g获取的是对象, stu.s_g_id获取到的int类型
        # 在flask中 stu.s_g获取的值为int类型
        stu.s_g = 1
        stu.save()
        return '关联学生和班级'


# 通过班级找学生
@blue.route('/selectstubygrade/<int:id>/')
def select_stu_by_grade(id):
    grade = Grade.query.get(id)
    # 通过班级对象.定义的relationship变量去获取学生的信息
    stus = grade.students  # 是一个列表

    # return render_template('grade_student.html',
    #                        stus=stus,
    #                        grade=grade
    #                        )
    return '通过班级查找学生信息'


# 通过学生找班级
@blue.route('/selectgradebystu/<int:id>/')
def select_grade_by_stu(id):
    stu = Students.query.get(id)
    # 通过学生对象.定义的backref参数去获取班级的信息
    grade = stu.grade

    # return render_template('student_grade.html',
    #                        grade=grade,
    #                        stu=stu)
    return '通过学生获取班级信息'


# 添加课程信息
@blue.route('/create_course_all/')
def create_course_all():
    course_names = ['数分', '高代', '几何', '离散', '复变', '运筹', '矩阵', '偏微分', '常微分', '有限元']
    course_list = []
    for course_name in course_names:
        course = Course()
        course.c_name = course_name
        course_list.append(course)
    db.session.add_all(course_list)
    db.session.commit()
    return '添加课程信息成功'


# 添加课程和学生的关联关系
@blue.route('/add_stu_cou/')
def add_stu_cou():
    stu = Students.query.get(15)
    # 学生的对象查找课程信息,stu.cou
    cou1 = Course.query.get(1)
    cou2 = Course.query.get(2)
    cou3 = Course.query.get(3)
    cou4 = Course.query.get(4)

    # 绑定学生和课程的关联关系
    # stu.cou.append(cou1)
    # stu.cou.append(cou2)
    # stu.cou.append(cou3)
    stu.save()

    return '金克斯选课成功'


# 通过课程查询学生的信息
@blue.route('/sel_stu_bycourse/')
def sel_stu_bycourse():
    course = Course.query.get(2)
    stus = course.students  # 查询的结果为BaseQuery 可以.all()查看
    return '通过课程查询学生的信息'


# 通过学生去查询课程的信息
@blue.route('/sel_course_bystu/')
def sel_course_bystu():
    stu = Students.query.get(15)
    courses = stu.cou
    # 查询的结果为列表  [ < Course1 >, < Course2 >, < Course3 >]

    return '通过课程查询学生的信息'


if __name__ == '__main__':
    pass
