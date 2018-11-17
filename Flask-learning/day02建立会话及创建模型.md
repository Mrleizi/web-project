### 1.会话上下文session

第一种:flask默认地将会话session存储在cookie中

> session['login_status'] = 1

第二种:指定数据库存取会话session数据

> 使用flask-session,将数据存储在Redis中
>
> 安装: pip install flask-session、 pip install redis
>
> 设置参数:SESSION_TYPE, SESSION_REDIS

```python
#session配置
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port=6379)
```



### 2.模板

父模板

> 负责搭建一个模板的骨架, 挖坑{% block %}

子模板

> 获取父模板坑的内容:{{ super() }}
>
> 继承: {% extends %}
>
> 包含: {% include 'xxx.html' %}

模板语法

标签:{% 标签 %}

> if/for/macro

变量:{{变量}}

> for 循环的内部变量 loop/looindex/loop.index0

过滤器，使用管道符'|'

> safe，length，striptags，capitalize，title

```html
 {{ content_h2 | safe }}
 {{ content_h2 | length }}
 <p style="color: crimson">{{ content_h2 | striptags }}</p>
 {{ content_h2 | striptags | capitalize }} <br>
 {{ content_h2 | striptags | title }}
 {{ content_h2 | safe | striptags | title }}
```

引入样式

> 第一种: src='/static/js/xxx.js',href='/static/css/xxx.css'
>
> 第二种:src='{{ url_for('static',fliename='js/xxx.js) }}'



### 3.模型

安装: 

> pip install flask-sqlalchemy， pip install pymysql

数据库连接地址 

> SQLALCHEMY_DATABASE_URI

```python
# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

在models.py文件中定义模型

**注: 若未定义 __ tablename __则在数据库中的表名为类名的小写**

> db=SQLAlchemy()
>
> db.Column()
>
> db.Integer
>
> db.String(10)



绑定flask对象并初始化

`db.init_app(app)`

用户初次出创建模型:`db.create_all()`

删除数据库中所有的表: `db.drop_all()`