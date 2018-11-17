from flask import Flask
from flask_script import Manager

from users.models import db
from users.views import user_blueprint, login_manager

app = Flask(__name__)
app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

app.config['SECRET_KEY'] = 'strong'

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask_login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 没有登录跳转地址
login_manager.login_view = 'user.login'

# 绑定
db.init_app(app)
login_manager.init_app(app)

manage = Manager(app=app)

if __name__ == '__main__':
    manage.run()
