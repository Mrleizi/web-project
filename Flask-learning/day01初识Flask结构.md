### 1. 环境搭建

创建虚拟环境 

> virtulaenv -p G:\python3.6.5\Scripts\python.exe --no-site-package flaskenv

安装Flask: 

> pip install Flask



### 2. 基于flask的最小的应用

创建hello.py文件

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def gello_world():
	return 'Hello World'

if __name__ == '__main__':

	app.run()
```



### 3. 路由

###### 路由匹配规则

>1.<id>:默认接收的类型的str
>
>2.<string:id>,指定id的类型为str
>
>3.<int:id>,指定id的类型为整型
>
>4.<float:id>,执行id的类型为浮点数
>
>5.<path:path>,指定接收的path为URL中的路径



1 | 2 接收的参数为字符串类型

```python
@blue.route('/get_id/<id>/')
def get_id(id):
	# 匹配str类型的id值
	return 'id:%s' % id
```

3 接收的参数为整型

```python
@blue.route('/get_int_id/<int:id>/')
def get_int_id(id):

	# 匹配int类型的id值
	return 'id:%d' % id
```

4 接收的参数为浮点数类型


```python
@blue.route('/get_float/<float:uid>/')
def get_float(uid):
  # 匹配float类型的值，不能匹配int类型
  return 'uid: %.2f' % uid
```

5 接收的参数为路径

```python
@blue.route('/get_path/<path:upath>/')
def get_path(upath):
  # 匹配URL路径
  return 'path: %s' % upath
```

###### 实现跳转

1、硬编码 

> redirect('url_prefix(前缀名)/蓝图路由')

`return redirect('/app/login/')`

2、反向解析 redirect(url_for('蓝图中定义的第一个参数.函数名', 参数名=value))

`return redirect(url_for('app.hello_world'))`



### 4. 服务启动

**run()中参数有如下:**

>debug 是否开启调试模式，开启后修改python的代码会自动重启
>
>port 启动指定服务器的端口号
>
>host主机，默认是127.0.0.1



**参数设置**:

>有两种途径来启用调试模式。一种是直接在应用对象上设置:
>
>app.debug = True
>app.run()
>另一种是作为 run 方法的一个参数传入:
>
>app.run(debug=True)
>两种方法的效果完全相同。



### 5. 修改启动方式，使用命令行参数启动服务

安装插件

>pip install flask-script
>
>调整代码 manager = Manager(app=‘自定义的flask对象’)
>
>启动的地方 manager.run()

启动命令

>python hello.py runserver -h 地址 -p 端口 -d -r
>其中：-h表示地址。-p表示端口。-d表示debug模式。-r表示自动重启



##### 蓝图Flask-Blueprint

安装: pip install flask-blueprint

第一步,获取蓝图对象

> 第一步，获取蓝图,指定蓝图别名为app
>
> blue = Blueprint('app', __name__)

第二步注册绑定

> 第二步，绑定蓝图blue和app的关系
>
> app.register_blueprint(blueprint=blue, url_prefix='/app')

url_for反向解析

> 语法:
>
> url_for('蓝图中定义的第一个参数.函数名', 参数名=value)

定义跳转：

```python
from flask import url_for, redirect

@blue.route('/redirect/')
def make_redirect():
    # 第一种方法
    return redirect('/hello/index/')
    # 第二种方法
    return redirect(url_for('first.index'))
```



### 6.请求上下文 request

获取GET请求传递的参数：

> request.args.get(key)/request.args.getlist(key)

例:`http://127.0.0.1:8092/app/index/?a=2&b=3`

```python
a = int(request.args.get('a'))
b = int(request.args.get('b'))
```



获取POST、PUT、PATCH、DELETE请求传递的参数：

> request.form.get(key)/request.form.getlist(key)

判断HTTP请求方式:

> request.method



### 7.创建响应

```python
# 创建响应
res_index = render_template('index.html')
res = make_response('人生苦短，我用Python', 200) #200是状态码
# 响应绑定cookie，set_cookie(key,value,max_age,expires)
# 删除cookie，delete_cookie(key)
return res
```



### 8.异常,捕捉

抛出异常

> from flask import abort
>
> abort(500)

捕捉

    @blue.errorhandler(500)
    def error500(exception):
      # return render_template('login.html'), 500
      return '捕捉异常，错误信息为: %s' % exception


