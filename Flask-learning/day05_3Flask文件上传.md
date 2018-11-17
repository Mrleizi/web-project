### 文件上传

#### 路径设置

```python
# 路径设置
import os

# 基础路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# static路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')

# templates路径
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# 上传路径
UPLOAD_DIR = os.path.join(os.path.join(STATIC_DIR, 'media'), 'upload')
```



##### 定义index.html首页

文件上传需要在form表单中添加enctype="multipart/form-data"

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
<h4 style="color: red;">这里是首页，需要登录后，才能访问</h4>
<h4 style="color: blue;">当前用户:{{ current_user.username }}</h4>
<img src="/static/media/{{ current_user.icons }}" alt="">
<form action="" method="post" enctype="multipart/form-data">
    头像: <input type="file" name="icons">
    <br>
    <input type="submit" value="上传头像">
</form>

<button><a href="{{ url_for('user.logout') }}" style="text-decoration: none">注销</a></button>
</body>
</html>
```



#### 获取页面上传的文件

flask中使用request.files获取页面上传的文件, 获取文件名:文件.filename

```python
@user_blueprint.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        # 获取图片
        icons = request.files.get('icons')
        if icons:
            # 保存save(path)
            # 1.jpg,png...使用正则表达式进行图片格式筛选
            if re.findall(".+(.JPEG|.jpeg|.JPG|.jpg|.GIF|.gif|.BMP|.bmp|.PNG|.png)$", icons.filename):
                file_path = os.path.join(UPLOAD_DIR, icons.filename)
                # file_path = os.path.join(UPLOAD_DIR, secure_filename(icons.filename))
                icons.save(file_path)
                # 保存user对象
                user = current_user
                user.icons = os.path.join('upload', icons.filename)
                user.save()
        return redirect(url_for('user.index'))
```


##### 