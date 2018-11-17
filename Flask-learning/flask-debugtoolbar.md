### 开发,页面调试工具debugtoolbar

#### 1.1安装

```python
pip install flask-debugtoolbar
```

#### 1.2 配置

```python
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
# 开启debug模式
app.debug = True

app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)
# 绑定并初始化app
toolbar.init_app(app)

if __name__ == '__main__':
    app.run()
```

