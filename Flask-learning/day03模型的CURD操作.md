### 1.模型CURD操作

**1.增**

单个创建 add()

```python
# 例子:
stu = Students()
stu.s_name = '雷克顿'
db.session.add(stu)
db.session.commit()
```

批量创建 add_all()

```python
# 例子:
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
```



**2.删 delete**

```python
stu = Students.query.filter(Students.id == id).first()
db.session.delete(stu)
db.session.commit()
```



**3.改**

```python
stu = Students.query.filter_by(id=id).first()
stu.s_name = '我爱罗'
db.session.add(stu)
db.session.commit()
```



**4.查**

>filter(),filter_by() 返回类型是querybase
>获取查询集
>
>all()
>filter(类名.属性名==xxx)
>filter_by(属性名=xxx)

```python
# 查询姓名为小明的学生
stu = Students.query.filter(Students.s_name == '小明')
stu = Students.query.filter_by(s_name='小明')

all , first()

# 查询结果为list
stus = Students.query.all() 

# 查询结果为对象
stu = Students.query.filter(Students.s_name == '小明').first()

# 执行sql 查询所有学生
# 查询结果为sql语句格式,可以fetchall()查看
sql = 'select * from students;'
stus = db.session.execute(sql)

stus.fetchall()
>>>
[(1, '小明', 20), (5, '我爱罗', 20), (6, '小李4', 27), (7, '小李5', 25), (33, '雷克顿', 20)]

# 查询id在某个范围之内的学生信息
select * from students where id in (1,2,3,4)
stus = Students.query.filter(Students.id.in_([1, 2, 3, 4]))

"""
filter(类名.属性名.运算符('xxx'))
filter(类名.属性 数学运算符  值)
"""
# 查询年龄大于19的学生信息
stus = Students.query.filter(Students.s_age > 19)
# 或者
stus=Students.query.filter(Students.s_age.gt(19))

# 模糊查询
# sql中语句如下
# select * from students where s_name like '%小%'
# select * from students where s_name like '小%'
# select * from students where s_name like '_明%' 第一个字随意,第二个字为明的同学

# 查询名字中包含有'小'字的同学
stu=Students.query.filter(Students.s_name.contains('小'))
stu=Students.query.filter(Students.s_name.like('%小%'))
# 查询名字以'小'开头的同学
stu=Students.query.filter(Students.s_name.startswith('小'))
stu=Students.query.filter(Students.s_name.like('小%'))
# 查询第一个字随意, 第二个字为'明'的同学
stu=Students.query.filter(Students.s_name.like('_明%'))

# get()获取主键对应的行数据
# 查询id=2的学生信息
stu = Students.query.get(5)

# 限制查询的结果集 offset/limit
stus = Students.query.limit(3)
stus = Students.query.offset(1).limit(3)

# 排序 order_by 
stus = Students.query.order_by('id') # 按id升序
stus = Students.query.order_by('-id') # 按id降序

"""and not or
# django中: filter(Q(A) | Q(B))
# flask中: filter(or_(A,B))
"""
# 查询姓名中包含'小'，并且年龄等于25
stus=Students.query.filter(Students.s_name.contains('小'),Students.s_age == 25)
stus=Students.query.filter(and_(Students.s_name.contains('小'),Students.s_age == 25))
# 查询姓名中包含'小'，或者年龄等于25
stus=Students.query.filter(or_(Students.s_name.contains('小'),Students.s_age == 25))
# 查询姓名中不包含'小'，且年龄等于20
stus=Students.query.filter(not_(Students.s_name.contains('小')),Students.s_age == 20)
```

