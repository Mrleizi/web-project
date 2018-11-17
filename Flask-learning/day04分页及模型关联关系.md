### 1.分页

```
模型.query.paginate(page,per_page,error_out) 
第一个参数是哪一页，第二个参数是一页的条数，第三个参数是是否输出错误信息
 students = Student.query.paginate(2, 4, False).items
```

###### paginate 属性说明

```
items      当前页面中的记录
query 	   分页的源查询
page       当前页数
prev_num   上一页的页数
next_num   下一页的页数
has_prev   如果有上一页,返回True
has_next   如果有下一页,返回True
pages      查询得到的总的页数
per_page   每页显示的记录数量
total      查询返回的记录总数
iter_pages 循环页码
```



###### 分页方法

```python
@blue.route('/paginate/')
def stu_page():	
  # 方法1 切片[:]
  page = int(request.args.get('page', 1))
  page_list = Students.query.all()[3 * page - 1:3 * page]

  # 方法2 offset+limit
  page = int(request.args.get('page', 1))
  stus = Students.query.offset((page - 1) * 3).limit(3)

  # 方法3 使用sql语句
  page = int(request.args.get('page', 1))
  sql = 'select * from students limit %s,%s' % ((page - 1) * 3, page * 3)
  stus = db.session.execute(sql)

  # 方法4 使用paginate()方法
  page = int(request.args.get('page', 1))
  paginate = Students.query.paginate(page, 3) # 参数1:显示某一页,参数2:当前页显示多少条数据
  stus = paginate.items  # 获取当前页的所有记录
  return render_template('stus.html', stus=stus, paginate=paginate)
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
  <table>
      <thead>
      <td>id</td>
      <td>姓名</td>
      <td>年龄</td>
      </thead>
      <tbody>
      {% for stu in stus %}
          <tr>
              <td>{{ stu.id }}</td>
              <td>{{ stu.s_name }}</td>
              <td>{{ stu.s_age }}</td>
          </tr>
      {% endfor %}
      </tbody>
  </table>
  <br>
  <p>当前{{ paginate.page }}页,共有{{ paginate.pages }}页</p>
  {% if paginate.has_prev %}
      <a href="{{ url_for('app.stu_page') }}?page={{ paginate.prev_num }}">上一页</a>
  {% endif %}

  {#{% for i in paginate.iter_pages() %}#}
  {% for i in paginate.iter_pages() %}
      {% if i %}
          <a href="{{ url_for('app.stu_page') }}?page={{ i }}">{{ i }}</a>
      {% else %}
          {# 若页数过多,省略一部分以...显示 #}
          <li style="display: inline"><a href="#">&hellip;</a></li>
      {% endif %}
  {% endfor %}

  {% if paginate.has_next %}
      <a href="{{ url_for('app.stu_page') }}?page={{ paginate.next_num }}">下一页</a>
  {% endif %}
  </body>
</html>
```



### 2.关联关系

### 2.1  -----  一对多

**一对多建立模型**

***

创建学生模型:

```python
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=False, nullable=False)
    s_age = db.Column(db.Integer, default=20)

    s_g = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)
    # 'grade.id' --- 表名.id

    __tablename__ = 'students'
```

创建班级模型

```python
class Grade(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name = db.Column(db.String(30), unique=True, nullable=False)

    students = db.relationship('Students', backref='grade',lazy=True)

    __tablename__ = 'grade'
```

**注:**若想建立一对一的关系, 在relationship中，添加一个字段unique=True

lazy 决定了 SQLAlchemy 什么时候从数据库中加载数据,有如下4个值**

**select:**/True: (which is the default) means that SQLAlchemy will load the data as necessary in one go using a standard select statement.

**joined:**/False: tells SQLAlchemy to load the relationship in the same query as the parent using a JOIN statement.

**subquery**: works like ‘joined’ but instead SQLAlchemy will use a subquery.

**dynamic**: is special and useful if you have many items. Instead of loading the items SQLAlchemy will return another query object which you can further refine before loading the items. This is usually what you want if you expect more than a handful of items for this relationship

```
select就是访问到属性的时候，就会全部加载该属性的数据。

joined则是在对关联的两个表进行join操作，从而获取到所有相关的对象。

dynamic则不一样，在访问属性的时候，并没有在内存中加载数据，而是返回一个query对象, 需要执行相应方法才可以获取对象，
```

**示例**

1.添加学生和班级的关联关系

```python
@blue.route('/rel_stu_grade/')
def rel_stu_grade():
    stud_ids = [15, 16, 17]
    for id in stud_ids:
        stu = Students.query.get(id)
        # 在django中 stu.s_g获取的是对象, stu.s_g_id获取到的int类型
        # 在flask中 stu.s_g获取的值为int类型  
        stu.s_g = 1
        db.session.add(stu)
        db.session.commit()
        return '关联学生和班级'
```



2.通过班级找学生信息

```python
@blue.route('/selectstubygrade/<int:id>/')
def select_stu_by_grade(id):
    grade = Grade.query.get(id)
    # 通过班级对象.定义的relationship变量去获取学生的信息
    stus = grade.students 
    # 查询结果是一个列表 [<Students 19>, <Students 22>, <Students 24>, <Students 25>, <Students 27>]
    return '通过班级查找学生信息'
```

3.通过学生查询班级信息

```python
@blue.route('/selectgradebystu/<int:id>/')
def select_grade_by_stu(id):
    stu = Students.query.get(id)
    # 通过学生对象.定义的backref参数去获取班级的信息
    grade = stu.grade
    # 查询结果是一个对象 <Grade 1>
    return '通过学生获取班级信息'
```

> 注: 表的外键由db.ForeignKey指定，传入的参数是表的字段。db.relations它声明的属性不作为表字段，第一个参数是关联类的名字，backref是一个反向身份的代理,相当于在Student类中添加了grade的属性。例如，有Grade实例grade和Student实例stu。grade.students.count()将会返回学生人数;stu.grade.first()将会返回学生的学院信息的Grade类实例。一般来讲db.relationship()会放在一这一边。

 

 

### 2.2   关联关系 ---- 多对多

**多对多建立模型**

***

1.创建中间表

```python
s_c = db.Table('s_c',
               db.Column('s_id', db.Integer, db.ForeignKey('students.id'), primary_key=True),
               db.Column('c_id', db.Integer, db.ForeignKey('course.id'), primary_key=True)
               )
```

2.创建学生模型

```python
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    s_name = db.Column(db.String(10), unique=False, nullable=False)
    s_age = db.Column(db.Integer, default=20)

    s_g = db.Column(db.Integer, db.ForeignKey('grade.id'), nullable=True)

    __tablename__ = 'students'
```

3.创建课程表模型

```python
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_name = db.Column(db.String(10), unique=True, nullable=False)

    students = db.relationship('Students', secondary=s_c, backref='cou', lazy='dynamic')

    __tablename__ = 'course'
```

>sc表由**db.Table声明**，我们不需要关心这张表，因为这张表将会由SQLAlchemy接管，它唯一的作用是作为students表和courses表关联表，所以必须在db.relationship()中指出**sencondary关联表参数**。lazy是指查询时的惰性求值的方式，这里有详细的参数说明，而db.backref是声明反向身份代理，其中的lazy参数是指明反向查询的惰性求值方式.



**示例**

1.添加学生和课程之间的关系

```python
@blue.route('/add_stu_cou/')
def add_stu_cou():
    stu = Students.query.get(15)
    # 学生的对象查找课程信息,stu.cou
    cou1 = Course.query.get(1)
    cou2 = Course.query.get(2)
    cou3 = Course.query.get(3)

    # 绑定学生和课程的关联关系
    stu.cou.append(cou1)
    stu.cou.append(cou2)
    stu.cou.append(cou3)
    db.session.add(stu)
    db.session.commit()

    return '金克斯选课成功'
```

2.删除学生和课程之间的关系

```python
stu = Student.query.get(s_id)
cou = Course.query.get(c_id)

cou.students.remove(stu)
db.session.commit()
```

3.通过课程查询学生的信息

以下定义在课程course的模型中，所以通过课程查询学生的信息，语法为课程的对象.students。如果知道学生的信息反过来找课程的信息，则使用backref的反向关联去查询，语语法为学生的对象.cou(反向)

```python
# 通过课程查询学生的信息
@blue.route('/sel_stu_bycourse/')
def sel_stu_bycourse():
    course = Course.query.get(2)
    stus = course.students  # 查询的结果为BaseQuery 可以.all()查看
    return '通过课程查询学生的信息'
```

4.通过学生去查询课程的信息

```python
@blue.route('/sel_course_bystu/')
def sel_course_bystu():
    stu = Students.query.get(15)
    courses = stu.cou
    # 查询的结果为列表  [ < Course1 >, < Course2 >, < Course3 >]

    return '通过课程查询学生的信息'
```

