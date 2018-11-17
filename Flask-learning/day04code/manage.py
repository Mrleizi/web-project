from flask_debugtoolbar import DebugToolbarExtension
from flask_script import Manager
from flask import Flask

from app.views import blue
from app.models import db

app = Flask(__name__)
app.register_blueprint(blueprint=blue, url_prefix='/app')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/flask01'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SECRET_KEY'] = 'secret_key'
# 开启debug模式
app.debug = True

# 初始化app和db
db.init_app(app)

# 初始化debugtoolbar和app
# toolbar = DebugToolbarExtension()
# toolbar.init_app(app)

manage = Manager(app=app)

if __name__ == '__main__':
    manage.run()
